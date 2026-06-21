import { readFileSync } from 'node:fs';

const html = readFileSync(new URL('../landing.html', import.meta.url), 'utf8');
const errors = [];
const heroSrc = '/assets/hero/paver-pool-deck-sealing.jpeg';
const tagAttrs = (tag) => Object.fromEntries([...tag.matchAll(/\s([\w:-]+)(?:=("[^"]*"|'[^']*'|[^\s>]+))?/g)].map(([, k, v = '']) => [k.toLowerCase(), v.replace(/^['"]|['"]$/g, '')]));
const imgTags = [...html.matchAll(/<img\b[^>]*>/gi)].map((m) => ({ tag: m[0], index: m.index, attrs: tagAttrs(m[0]) }));
const linkTags = [...html.matchAll(/<link\b[^>]*>/gi)].map((m) => ({ tag: m[0], index: m.index, attrs: tagAttrs(m[0]) }));
const before = (needle) => {
  const i = html.indexOf(needle);
  return i === -1 ? Infinity : i;
};
const heroSectionIndex = before('<section class="lp-hero"');
const trustIndex = before('<!-- Trust strip -->');
const firstContentIndex = before('<!-- Transparent Pricing -->');

const fail = (message) => errors.push(message);

const heroImgs = imgTags.filter(({ attrs }) => attrs.id === 'hero_lcp');
if (heroImgs.length !== 1) fail(`Expected exactly one #hero_lcp image, found ${heroImgs.length}.`);
const hero = heroImgs[0]?.attrs || {};
if (hero.src !== heroSrc) fail(`#hero_lcp src must be ${heroSrc}; found ${hero.src || '(missing)'}.`);
if (hero.fetchpriority !== 'high') fail('#hero_lcp must be the only fetchpriority="high" image.');
if (hero.loading !== 'eager') fail('#hero_lcp must be the only loading="eager" image.');
if (hero.decoding !== 'async') fail('#hero_lcp must use decoding="async".');
if (hero.width !== '1920' || hero.height !== '1080') fail('#hero_lcp must reserve 1920x1080 dimensions.');
if ('srcset' in hero) fail('#hero_lcp must not use srcset.');

const highImages = imgTags.filter(({ attrs }) => attrs.fetchpriority === 'high');
const eagerImages = imgTags.filter(({ attrs }) => attrs.loading === 'eager');
if (highImages.length !== 1 || highImages[0]?.attrs.id !== 'hero_lcp') fail(`Only #hero_lcp may use fetchpriority="high"; found ${highImages.length}.`);
if (eagerImages.length !== 1 || eagerImages[0]?.attrs.id !== 'hero_lcp') fail(`Only #hero_lcp may use loading="eager"; found ${eagerImages.length}.`);

for (const { attrs } of imgTags) {
  if (attrs.id === 'hero_lcp') continue;
  if (attrs.loading !== 'lazy') fail(`Non-hero image must use loading="lazy": ${attrs.src || '(missing src)'}.`);
  if (attrs.decoding !== 'async') fail(`Non-hero image must use decoding="async": ${attrs.src || '(missing src)'}.`);
}

const imagePreloads = linkTags.filter(({ attrs }) => attrs.rel === 'preload' && attrs.as === 'image');
if (imagePreloads.length !== 1) fail(`Expected exactly one image preload, found ${imagePreloads.length}.`);
if (imagePreloads[0]?.attrs.id !== 'preload_lcp' || imagePreloads[0]?.attrs.href !== heroSrc) fail('The only image preload must be #preload_lcp and must exactly match #hero_lcp src.');


const cssText = (html.match(/<style>\s*([\s\S]*?)<\/style>/i)?.[1] || '').replace(/\/\*[\s\S]*?\*\//g, '');
const declarationsFor = (selector) => {
  const escaped = selector.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const matches = [...cssText.matchAll(new RegExp(`${escaped}\\s*\\{([^}]*)\\}`, 'g'))];
  return matches.map(([, body]) => body).join('\n');
};
const hasDecl = (selector, property, value) => new RegExp(`${property}\\s*:\\s*${value}\\s*(?:;|$)`, 'i').test(declarationsFor(selector));

if (!hasDecl('.lp-header', 'position', 'relative')) fail('.lp-header must be position: relative to create a locked header stacking context.');
if (!hasDecl('.lp-header', 'z-index', '10000')) fail('.lp-header must keep z-index: 10000.');
if (!hasDecl('.lp-header', 'background', '#fff')) fail('.lp-header must keep an opaque #fff background.');
if (!hasDecl('.lp-hero', 'position', 'relative')) fail('.lp-hero must be position: relative.');
if (!hasDecl('.lp-hero', 'z-index', '1')) fail('.lp-hero must keep z-index: 1 so it cannot overlap the header.');
if (!hasDecl('.lp-hero-img', 'position', 'absolute')) fail('.lp-hero-img must be position: absolute.');
if (!hasDecl('.lp-hero-img', 'inset', '0')) fail('.lp-hero-img must use inset: 0.');
if (!hasDecl('.lp-hero-img', 'z-index', '0')) fail('.lp-hero-img must stay behind hero content with z-index: 0.');
if (!hasDecl('.lp-hero-content', 'z-index', '2')) fail('.lp-hero-content must keep z-index: 2.');
if (!hasDecl('.mobile-contactbar', 'z-index', '9000')) fail('.mobile-contactbar must use z-index: 9000 so it stays below the header layer.');

if (/<picture\b/i.test(html) || /<source\b/i.test(html)) fail('No picture/source fallbacks are allowed on /landing.');
if (/srcset\s*=/i.test(html)) fail('No srcset attributes are allowed on /landing.');
if (/background-image\s*:/i.test(html)) fail('No background-image visuals are allowed on /landing.');

const preHeroImages = imgTags.filter(({ index, attrs }) => index < heroSectionIndex || (index > heroSectionIndex && index < trustIndex && attrs.id !== 'hero_lcp'));
if (preHeroImages.length) fail(`No image may appear before trust strip except #hero_lcp; found ${preHeroImages.map(({ attrs }) => attrs.src || attrs.id || '(unknown)').join(', ')}.`);
const earlyNonHeroImages = imgTags.filter(({ index, attrs }) => attrs.id !== 'hero_lcp' && index < firstContentIndex);
if (earlyNonHeroImages.length) fail(`Non-hero images must appear after the first content section starts; found ${earlyNonHeroImages.map(({ attrs }) => attrs.src || '(unknown)').join(', ')}.`);

if (errors.length) {
  console.error('Landing LCP architecture validation failed:');
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}
console.log('Landing LCP architecture validation passed.');
