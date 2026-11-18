// Builds site themes from Omarchy palettes (colors.toml) into src/styles/themes.css + src/data/themes.json.
// Run locally when Omarchy themes change: `npm run themes`. Output is committed, so CI does not need Omarchy.
import { readdirSync, readFileSync, existsSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const SOURCES = [join(homedir(), ".config/omarchy/themes"), "/usr/share/omarchy/themes"];

const hex = (h) => {
  h = h.replace("#", "");
  if (h.length === 3) h = [...h].map((c) => c + c).join("");
  return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16));
};
const toHex = (rgb) => "#" + rgb.map((v) => Math.round(Math.max(0, Math.min(255, v))).toString(16).padStart(2, "0")).join("");
const mix = (a, b, t) => toHex(hex(a).map((v, i) => v + (hex(b)[i] - v) * t)); // t = share of b
const lum = (h) => {
  const [r, g, b] = hex(h).map((v) => {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const contrast = (a, b) => {
  const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p);
  return (x + 0.05) / (y + 0.05);
};
// nudge fg towards "towards" until it reaches the target contrast against bg
const ensure = (fg, bg, target, towards) => {
  let c = fg;
  for (let t = 0; contrast(c, bg) < target && t <= 1; t += 0.05) c = mix(fg, towards, t);
  return c;
};

function parse(file) {
  const out = {};
  for (const line of readFileSync(file, "utf8").split("\n")) {
    const m = line.match(/^\s*([a-z_]+)\s*=\s*"([^"]+)"/);
    if (m) out[m[1]] = m[2];
  }
  return out;
}

function tokens(c) {
  const light = c.mode === "light";
  const bg = c.background;
  const fg = c.foreground;
  const heading = c.bright_foreground ?? fg;
  const white = "#ffffff", black = "#000000";
  const accent = ensure(c.accent ?? c.blue, bg, 3, light ? black : white);
  const accent2 = (c.accent ?? "").toLowerCase() === (c.blue ?? "").toLowerCase() ? c.cyan ?? c.magenta : c.blue ?? c.cyan;
  const deep = light ? fg : c.darker_background ?? mix(bg, black, 0.35);
  const onDeep = light ? bg : heading;
  return {
    "--bg": bg,
    "--surface": light ? mix(bg, white, 0.65) : c.lighter_background ?? mix(bg, white, 0.06),
    "--surface-2": light ? mix(bg, fg, 0.07) : c.selection ?? mix(bg, white, 0.1),
    "--heading": heading,
    "--text": fg,
    "--muted": ensure(c.dark_foreground ?? mix(fg, bg, 0.35), bg, 4.5, light ? black : white),
    "--line": mix(bg, fg, 0.12),
    "--accent": accent,
    "--accent-hover": mix(accent, light ? black : white, 0.15),
    "--accent-2": accent2 ?? accent,
    "--on-accent": contrast(white, accent) >= contrast(bg, accent) ? white : bg,
    "--deep": deep,
    "--accent-deep": ensure(accent, deep, 3.5, onDeep),
    "--on-deep": onDeep,
    "--deep-text": mix(onDeep, deep, 0.22),
    "--terrain": mix(bg, fg, light ? 0.13 : 0.1),
    "--terrain-deep": mix(deep, onDeep, 0.12),
    "--shadow": light ? fg : black,
    "--neu-hi": light ? mix(bg, white, 0.7) : mix(bg, white, 0.05),
    "--neu-lo": light ? mix(bg, fg, 0.16) : mix(bg, black, 0.45),
    "--photo-filter": light ? "none" : "brightness(0.92)",
  };
}

const themes = [];
const seen = new Set();
for (const dir of SOURCES) {
  if (!existsSync(dir)) continue;
  for (const id of readdirSync(dir).sort()) {
    const file = join(dir, id, "colors.toml");
    if (seen.has(id) || !existsSync(file)) continue;
    const c = parse(file);
    if (!c.background || !c.foreground) continue;
    seen.add(id);
    const name = id === "priver" ? "Priver (my Omarchy)" : id.split("-").map((w) => w[0].toUpperCase() + w.slice(1)).join(" ");
    themes.push({ id: `omarchy-${id}`, name, mode: c.mode === "light" ? "light" : "dark", tokens: tokens(c) });
  }
}
// user's own Omarchy theme first
themes.sort((a, b) => (a.id === "omarchy-priver" ? -1 : b.id === "omarchy-priver" ? 1 : a.name.localeCompare(b.name)));

const brand = [
  {
    id: "light", name: "Depriver Light", mode: "light",
    tokens: {
      "--bg": "#f7f6f2", "--surface": "#ffffff", "--surface-2": "#eef1f6", "--heading": "#192e28", "--text": "#3b414d",
      "--muted": "#5c626e", "--line": "#e2e4e9", "--accent": "#366958", "--accent-hover": "#285443", "--accent-2": "#a9c4f5",
      "--on-accent": "#ffffff", "--deep": "#192e28", "--accent-deep": "#366958", "--on-deep": "#ffffff", "--deep-text": "#bdcec3",
      "--terrain": "#d3d9e6", "--terrain-deep": "#1f3a6b", "--shadow": "#192e28", "--neu-hi": "#ffffff", "--neu-lo": "#d9dde6", "--photo-filter": "none",
    },
  },
  {
    id: "dark", name: "Depriver Dark", mode: "dark",
    tokens: {
      "--bg": "#111c19", "--surface": "#192722", "--surface-2": "#23352e", "--heading": "#f4f6fb", "--text": "#d1dbd5",
      "--muted": "#a4b6ab", "--line": "#33463d", "--accent": "#82b59a", "--accent-hover": "#a6cfb6", "--accent-2": "#a9c4f5",
      "--on-accent": "#111c19", "--deep": "#172b22", "--accent-deep": "#82b59a", "--on-deep": "#ffffff", "--deep-text": "#bdcec3", "--terrain": "#233d30",
      "--terrain-deep": "#304b3b", "--shadow": "#000000", "--neu-hi": "#0c1b37", "--neu-lo": "#030a17", "--photo-filter": "brightness(0.92)",
    },
  },
];

let css = "/* Generated by scripts/omarchy-themes.mjs. Do not edit by hand. */\n";
const block = (sel, t, mode) =>
  `${sel} {\n${Object.entries(t).map(([k, v]) => `  ${k}: ${v};`).join("\n")}\n  color-scheme: ${mode};\n}\n`;
// [data-theme] works on any element, so the theme menu can preview a theme inside a small card
css += block('[data-theme="light"]', brand[0].tokens, "light");
css += block('[data-theme="dark"]', brand[1].tokens, "dark");
css += `@media (prefers-color-scheme: dark) {\n${block(':root:not([data-theme])', brand[1].tokens, "dark").replace(/^/gm, "  ")}}\n`;
for (const t of themes) css += block(`[data-theme="${t.id}"]`, t.tokens, t.mode);
writeFileSync(new URL("../src/styles/themes.css", import.meta.url), css);

const list = [...brand, ...themes].map((t) => {
  const tk = t.tokens;
  const group = t.id.startsWith("omarchy-") ? (t.mode === "light" ? "Omarchy · Light" : "Omarchy · Dark") : "Depriver";
  return { id: t.id, name: t.name, mode: t.mode, group, swatch: [tk["--bg"], tk["--deep"], tk["--accent"], tk["--accent-2"]] };
});
writeFileSync(new URL("../src/data/themes.json", import.meta.url), JSON.stringify(list, null, 2));
console.log(`${list.length} themes written`);
