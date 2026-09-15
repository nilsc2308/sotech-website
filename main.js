(() => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const mobile = () => window.innerWidth <= 1020;
  if (reduce) document.documentElement.classList.add('no-motion');
  gsap.registerPlugin(ScrollTrigger);
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  const $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const fmt = (n, d = 0) => n.toLocaleString('de-DE', { minimumFractionDigits: d, maximumFractionDigits: d });

  // ---------- Lenis (weiches Scrollen) ----------
  let lenis;
  if (!reduce) {
    lenis = new Lenis({ lerp: 0.09, smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }
  const scrollToEl = (el, off = -30) => lenis ? lenis.scrollTo(el, { offset: off, duration: 1.3 }) : el.scrollIntoView({ behavior: 'smooth' });
  $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    const id = a.getAttribute('href'); if (id.length < 2) return;
    const el = $(id); if (!el) return;
    e.preventDefault(); closeMenu(); scrollToEl(el);
  }));

  // ---------- Navigation: minimal + Vollbild-Menü ----------
  const nav = $('#nav'), menuBtn = $('#menuBtn'), menu = $('#menu');
  const hasHero = !!($('.scene') || $('.ph') || $('.err-page'));
  if (hasHero) document.body.classList.add('over-hero');
  const navCheck = () => nav.classList.toggle('solid', window.scrollY > (hasHero ? innerHeight * .7 : 30));
  addEventListener('scroll', navCheck, { passive: true }); navCheck();
  let lastFocus;
  const closeMenu = () => {
    if (!menu.classList.contains('open')) return;
    document.body.classList.remove('menu-open'); menu.classList.remove('open');
    menuBtn.setAttribute('aria-expanded', 'false'); menuBtn.querySelector('.lbl').textContent = 'Menü';
    lenis && lenis.start(); lastFocus && lastFocus.focus();
  };
  const openMenu = () => {
    lastFocus = document.activeElement;
    document.body.classList.add('menu-open'); menu.classList.add('open');
    menuBtn.setAttribute('aria-expanded', 'true'); menuBtn.querySelector('.lbl').textContent = 'Schließen';
    lenis && lenis.stop(); setTimeout(() => menu.querySelector('a').focus(), 500);
  };
  menuBtn.addEventListener('click', () => menu.classList.contains('open') ? closeMenu() : openMenu());
  $$('a', menu).forEach(a => a.addEventListener('click', () => { if (a.getAttribute('href').startsWith('#')) closeMenu(); }));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && menu.classList.contains('open')) { closeMenu(); menuBtn.focus(); }
    if (e.key === 'Tab' && menu.classList.contains('open')) { // Fokus im Menü halten
      const f = $$('a, button', menu).filter(x => x.offsetParent); const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); menuBtn.focus(); }
    }
  });
  $$('.menu a.active').forEach(a => a.setAttribute('aria-current', 'page'));

  // ---------- Wort-für-Wort-Reveals ----------
  $$('.split').forEach(el => {
    const words = el.textContent.trim().split(/\s+/);
    el.setAttribute('aria-label', words.join(' '));
    el.innerHTML = words.map(w => `<span class="split-line" aria-hidden="true"><span class="w">${w}</span></span>`).join(' ');
  });

  // ---------- Vorhang + Brand-Intro (nur beim ersten Besuch) ----------
  const intro = $('.curtain.intro');
  let seen = false; try { seen = sessionStorage.getItem('sotech-intro'); } catch (e) {}
  if (intro && !seen && !reduce) {
    try { sessionStorage.setItem('sotech-intro', '1'); } catch (e) {}
    document.body.classList.add('intro-on');
    setTimeout(() => document.body.classList.add('ready'), 1250);
  } else requestAnimationFrame(() => document.body.classList.add('ready'));
  $$('a[href$=".html"], a[href*=".html#"], a[href*=".html?"]').forEach(a => a.addEventListener('click', e => {
    if (e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank' || reduce) return;
    const href = a.getAttribute('href'); if (/^https?:/.test(href)) return;
    const [path] = href.split(/[#?]/), here = location.pathname.split('/').pop() || 'index.html';
    if (path === here && href.includes('#')) { const el = $('#' + href.split('#')[1]); if (el) { e.preventDefault(); closeMenu(); scrollToEl(el); return; } }
    e.preventDefault(); closeMenu(); document.body.classList.add('leaving');
    setTimeout(() => location.href = href, 600);
  }));
  addEventListener('pageshow', e => { if (e.persisted) document.body.classList.remove('leaving'); });

  // ---------- Fortschrittsbalken + Sticky-CTA ----------
  const prog = $('#progress');
  if (prog) ScrollTrigger.create({ onUpdate: s => prog.style.transform = `scaleX(${s.progress})` });
  const sticky = $('.sticky-cta');
  if (sticky) { const first = $('.scene') || $('.ph'); ScrollTrigger.create({ start: () => (first ? first.offsetHeight - innerHeight * .5 : 300), end: 'max', onToggle: t => sticky.classList.toggle('show', t.isActive) }); }
  $$('.totop').forEach(a => a.addEventListener('click', e => { e.preventDefault(); lenis ? lenis.scrollTo(0, { duration: 1.3 }) : scrollTo({ top: 0, behavior: 'smooth' }); }));

  // ---------- Magnetische Buttons + Lichtreflex, 3D-Tilt ----------
  const fine = matchMedia('(hover:hover) and (pointer:fine)').matches;
  if (fine && !reduce) {
    $$('.btn').forEach(b => {
      b.addEventListener('mousemove', e => {
        const r = b.getBoundingClientRect(); const x = e.clientX - r.left, y = e.clientY - r.top;
        b.style.setProperty('--mx', x + 'px'); b.style.setProperty('--my', y + 'px');
        gsap.to(b, { x: (x - r.width / 2) * .22, y: (y - r.height / 2) * .32, duration: .5, ease: 'power3.out' });
      });
      b.addEventListener('mouseleave', () => gsap.to(b, { x: 0, y: 0, duration: .8, ease: 'elastic.out(1,.5)' }));
    });
    $$('.tilt').forEach(c => {
      c.addEventListener('mousemove', e => { const r = c.getBoundingClientRect(); const px = (e.clientX - r.left) / r.width - .5, py = (e.clientY - r.top) / r.height - .5; gsap.to(c, { rotateY: px * 8, rotateX: -py * 8, transformPerspective: 900, duration: .5, ease: 'power2.out' }); });
      c.addEventListener('mouseleave', () => gsap.to(c, { rotateY: 0, rotateX: 0, duration: .9, ease: 'power3.out' }));
    });
  }

  // ---------- Allgemeine Scroll-Reveals ----------
  if (!reduce) {
    $$('.split').forEach(el => gsap.to($$('.w', el), { y: 0, duration: 1, ease: 'power4.out', stagger: .045, scrollTrigger: { trigger: el, start: 'top 88%' } }));
    ScrollTrigger.batch('.reveal', { start: 'top 90%', onEnter: els => gsap.to(els, { opacity: 1, y: 0, duration: 1, ease: 'power3.out', stagger: .08, overwrite: true }) });
  }

  // ---------- Foto-Scroll-Through: 5 Fotos, 5 Blenden (Iris, Streifen-Vorhang, Flüssig-Wipe, Kacheln, Zoom-Dive + Blitz) ----------
  const scene = $('.scene');
  if (scene) {
    // Streifen und Kacheln aus dem jeweiligen Foto bauen
    const l3 = $('.l3', scene), l5 = $('.l5', scene); const small = innerWidth <= 820;
    $('.strips', l3).innerHTML = Array.from({ length: 8 }, (_, i) => `<i style="background-position:0 ${i / 7 * 100}%"></i>`).join('');
    $('.tiles', l5).innerHTML = Array.from({ length: 12 }, (_, i) => `<i style="background-position:${(i % 4) / 3 * 100}% ${Math.floor(i / 4) / 2 * 100}%"></i>`).join('');
    // Fotos 2–5 erst nach dem Laden der Seite nachziehen (Ladegröße bis „load“ klein halten)
    let lateDone = false; const late = () => { if (lateDone) return; lateDone = true;
      $$('img[data-src]', scene).forEach(im => { im.srcset = im.dataset.srcset; im.src = im.dataset.src; });
      $$('.strips i', l3).forEach(i => i.style.backgroundImage = `url(${small ? l3.dataset.imgM : l3.dataset.img})`);
      $$('.tiles i', l5).forEach(i => i.style.backgroundImage = `url(${small ? l5.dataset.imgM : l5.dataset.img})`); };
    if (document.readyState === 'complete') setTimeout(late, 300); else addEventListener('load', () => setTimeout(late, 300));
    addEventListener('scroll', late, { once: true, passive: true });
    const caps = $$('.cap', scene);
    caps.forEach(c => $$('h1, h2, p:not(.k)', c).forEach(el => { const words = el.textContent.trim().split(/\s+/); el.setAttribute('aria-label', words.join(' ')); el.innerHTML = words.map(w => `<span class="w" aria-hidden="true">${w}</span>`).join(' '); }));
    if (!reduce) {
      const prog = document.createElement('div'); prog.className = 'prog'; prog.setAttribute('aria-hidden', 'true'); prog.innerHTML = '<i></i>'.repeat(5); $('.stage', scene).appendChild(prog); const bars = $$('i', prog);
      const capIn = (c, t) => tl.set(c, { opacity: 1, visibility: 'visible' }, t).fromTo($$('.w', c), { yPercent: 110, opacity: 0 }, { yPercent: 0, opacity: 1, duration: .35, stagger: .02, ease: 'power3.out', immediateRender: false }, t);
      const capOut = (c, t) => tl.to($$('.w', c), { yPercent: -60, opacity: 0, duration: .2, stagger: .01, ease: 'power2.in' }, t).set(c, { visibility: 'hidden' }, t + .3);
      const wave = p => { // Flüssig-Wipe: Wellenkante von oben nach unten
        const pts = ['0 0', '100% 0']; const y = -25 + p * 150;
        for (let i = 12; i >= 0; i--) { const x = i / 12 * 100; pts.push(`${x}% ${y + Math.sin(i / 12 * Math.PI * 2 + p * 4) * 9 + Math.cos(i / 12 * Math.PI * 3) * 5}%`); }
        return `polygon(${pts.join(',')})`;
      };
      const L = i => $('.l' + i, scene);
      const tl = gsap.timeline({ scrollTrigger: { trigger: scene, start: 'top top', end: 'bottom bottom', scrub: .5, onUpdate: s => bars.forEach((b, i) => b.style.setProperty('--p', clamp(s.progress * 5.6 - i, 0, 1))) } });
      // 1: Ruhe + Zoom
      tl.fromTo($('img', L(1)), { scale: 1.06 }, { scale: 1.18, duration: 1.1, ease: 'none' }, 0);
      capOut($('.cap', L(1)), .75);
      // 2: Iris-Blende
      tl.fromTo($('img', L(2)), { scale: 1.25 }, { scale: 1.05, duration: 1, ease: 'power2.out' }, .9)
        .to(L(2), { clipPath: 'circle(85% at 50% 55%)', duration: .6, ease: 'power2.inOut' }, .95);
      capIn($('.cap', L(2)), 1.35); capOut($('.cap', L(2)), 1.85);
      // 3: Vorhang aus horizontalen Streifen
      tl.to($$('.strips i', L(3)), { scaleX: 1, duration: .45, stagger: { each: .05, from: 'start' }, ease: 'power3.inOut' }, 2.0);
      capIn($('.cap', L(3)), 2.5); capOut($('.cap', L(3)), 3.0);
      // 4: Flüssig-Wipe (clip-path-Polygon mit Wellenkante)
      const wv = { p: 0 };
      tl.to(wv, { p: 1, duration: .6, ease: 'power2.inOut', onUpdate: () => L(4).style.clipPath = wave(wv.p) }, 3.15)
        .fromTo($('img', L(4)), { scale: 1.15, y: -30 }, { scale: 1.02, y: 0, duration: 1, ease: 'power2.out' }, 3.15);
      capIn($('.cap', L(4)), 3.65); capOut($('.cap', L(4)), 4.15);
      // 5: Kachel-Montage → Zoom-Dive + Lichtblitz
      tl.to($$('.tiles i', L(5)), { scale: 1, opacity: 1, duration: .4, stagger: { each: .04, from: 'random' }, ease: 'back.out(1.4)' }, 4.3)
        .to($('.dive', L(5)), { opacity: 1, duration: .15 }, 4.95)
        .to($('.dive', L(5)), { scale: 2.6, duration: .7, ease: 'power3.in' }, 5.0)
        .to($('.flash', L(5)), { opacity: 1, duration: .18, ease: 'power2.in' }, 5.55)
        .to($('.flash', L(5)), { opacity: 0, duration: .35, ease: 'power2.out' }, 5.73)
        .set($('.dive', L(5)), { scale: 1.15 }, 5.73)
        .to($('.dive', L(5)), { scale: 1.02, duration: .8, ease: 'power2.out' }, 5.73)
        .to($('.final', scene), { opacity: 1, visibility: 'visible', duration: .3 }, 5.7);
      capIn($('.final .cap', scene), 5.85);
      tl.to({}, { duration: .5 });
    } else $$('.w', scene).forEach(w => w.style.opacity = 1);
  }

  // ---------- Zahl schrumpft und rastet in den Text ein ----------
  const year = $('.year');
  if (year && !reduce) {
    const big = $('.big', year), copy = $('.copy', year), slot = $('.slot', year), stage = $('.stage', year);
    const target = () => {
      const s = stage.getBoundingClientRect(), r = slot.getBoundingClientRect();
      const fs = parseFloat(getComputedStyle(slot).fontSize) / parseFloat(getComputedStyle(big).fontSize);
      return { x: r.left + r.width / 2 - (s.left + s.width / 2), y: r.top + r.height / 2 - (s.top + s.height / 2), scale: fs };
    };
    const tl = gsap.timeline({ scrollTrigger: { trigger: year, start: 'top top', end: 'bottom bottom', scrub: .5, invalidateOnRefresh: true } });
    tl.fromTo(big, { xPercent: -50, yPercent: -50, x: 0, y: 0, scale: 1 }, { x: () => target().x, y: () => target().y, scale: () => target().scale, duration: 1, ease: 'power2.inOut' })
      .fromTo(copy, { opacity: 0 }, { opacity: 1, duration: .3, ease: 'power2.out' }, .92)
      .to({}, { duration: .35 });
  }

  // ---------- Akkordeon-Galerie ----------
  const acc = $('.acc');
  if (acc) {
    const strips = $$('.strip', acc);
    const activate = s => strips.forEach(x => { x.classList.toggle('on', x === s); x.setAttribute('aria-expanded', String(x === s)); });
    strips.forEach(s => {
      s.addEventListener('mouseenter', () => { if (fine) activate(s); });
      s.addEventListener('click', e => { if (s.classList.contains('on')) { if (!e.target.closest('a')) location.href = s.dataset.href; } else { e.preventDefault(); activate(s); } });
      s.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); s.classList.contains('on') ? location.href = s.dataset.href : activate(s); } });
    });
    if (!reduce) gsap.to(strips, { clipPath: 'inset(0% 0 0% 0)', ease: 'power3.out', stagger: .12, scrollTrigger: { trigger: acc, start: 'top 85%', end: 'top 35%', scrub: .4 } });
  }

  // ---------- Signature: 24-Stunden-Uhr, Tag → Nacht ----------
  const day = $('.day');
  if (day) {
    const R = 210, C = 250; // Kreisradius, Mittelpunkt
    const ang = h => (h / 24) * Math.PI * 2 + Math.PI / 2; // 0 h unten, 12 h oben
    const pos = h => ({ x: C + R * Math.cos(ang(h)), y: C + R * Math.sin(ang(h)) });
    const arc = $('.arc', day); const a1 = pos(6), a2 = pos(18);
    arc.setAttribute('d', `M ${a1.x} ${a1.y} A ${R} ${R} 0 0 1 ${a2.x} ${a2.y}`);
    const len = arc.getTotalLength(); arc.style.strokeDasharray = len; arc.style.strokeDashoffset = len;
    // Ticks + Beschriftung
    const ticks = $('.ticks', day); let t = '';
    for (let h = 0; h < 24; h++) { const big = h % 6 === 0, p1 = pos(h), a = ang(h); const l = big ? 14 : 7; t += `<line class="tick${big ? ' h' : ''}" x1="${p1.x}" y1="${p1.y}" x2="${C + (R - l) * Math.cos(a)}" y2="${C + (R - l) * Math.sin(a)}"/>`; if (big) { const q = { x: C + (R + 26) * Math.cos(a), y: C + (R + 26) * Math.sin(a) + 5 }; t += `<text x="${q.x}" y="${q.y}">${String(h).padStart(2, '0')}</text>`; } }
    ticks.innerHTML = t;
    const orb = $('.orb', day), moon = $('.moon', day), clock = $('.clock', day), bat = $('.bat-fill', day), glow = $('.roof-glow', day), wins = $$('.win.lit', day), flowD = $('.flow.d', day), flowN = $('.flow.n', day), states = $$('.st', day), stage = $('.stage', day), hl = $('.hl', day);
    const BAT = { y0: 318, h: 44 };
    const setHour = h => { // h in [5, 29)
      const hh = ((h % 24) + 24) % 24; const p = pos(hh);
      const up = Math.max(0, Math.sin((hh - 6) / 12 * Math.PI)); // Sonnenhöhe 0..1 zwischen 6 und 18 Uhr
      orb.setAttribute('cx', p.x); orb.setAttribute('cy', p.y); orb.style.opacity = hh >= 5.5 && hh <= 19 ? 1 : 0;
      moon.setAttribute('cx', p.x); moon.setAttribute('cy', p.y); moon.style.opacity = hh < 5.5 || hh > 19 ? 1 : 0;
      arc.style.strokeDashoffset = len * (1 - clamp((hh - 6) / 12, 0, 1)) * (hh > 18 && hh < 6 ? 0 : 1);
      if (hh < 6) arc.style.strokeDashoffset = len;
      clock.textContent = `${String(Math.floor(hh)).padStart(2, '0')}:${String(Math.floor((hh % 1) * 60)).padStart(2, '0')}`;
      hl.textContent = hh < 9 ? 'Morgen' : hh < 16 ? 'Mittag' : hh < 21 ? 'Abend' : 'Nacht';
      // Speicherstand: lädt über den Tag, entlädt nachts (schematisch)
      const soc = hh < 5 ? .55 - (hh / 5) * .3 : hh < 8 ? .25 : hh < 15 ? .25 + ((hh - 8) / 7) * .75 : hh < 18 ? 1 - ((hh - 15) / 3) * .1 : .9 - ((hh - 18) / 6) * .35;
      bat.setAttribute('y', BAT.y0 + BAT.h * (1 - soc)); bat.setAttribute('height', BAT.h * soc);
      glow.style.opacity = up * .75;
      const night = hh < 7 || hh > 19; wins.forEach(w => w.style.opacity = night ? .9 : 0);
      flowD.style.opacity = up > .15 ? 1 : 0; flowN.style.opacity = night || hh > 17 ? 1 : 0;
      // Hintergrund: Gelb (Mittag) → Orange (Abend) → Nacht
      const bgKey = [[5, 62], [8, 22], [12, 0], [16, 12], [18.5, 40], [21, 80], [24, 100], [29, 62]];
      let y = 100; for (let i = 0; i < bgKey.length - 1; i++) { const [h0, v0] = bgKey[i], [h1, v1] = bgKey[i + 1]; if (h >= h0 && h <= h1) { y = v0 + (v1 - v0) * (h - h0) / (h1 - h0); break; } }
      stage.style.backgroundPosition = `0 ${y}%`; stage.classList.toggle('n', hh >= 17.2 || hh < 6.2);
      const si = hh >= 5 && hh < 9 ? 0 : hh >= 9 && hh < 16 ? 1 : hh >= 16 && hh < 21 ? 2 : 3;
      states.forEach((s, i) => { if (i === si && !s.classList.contains('on')) { s.classList.add('on'); gsap.fromTo(s, { opacity: 0, y: 24, visibility: 'visible' }, { opacity: 1, y: 0, duration: .45, delay: .18, ease: 'power3.out', overwrite: true }); } else if (i !== si && s.classList.contains('on')) { s.classList.remove('on'); gsap.to(s, { opacity: 0, y: -16, duration: .18, overwrite: true, onComplete: () => s.style.visibility = 'hidden' }); } });
    };
    if (reduce) { states.forEach(s => { s.style.opacity = 1; s.style.visibility = 'visible'; }); setHour(12); states.forEach(s => { s.style.opacity = 1; s.style.visibility = 'visible'; }); }
    else { const o = { h: 5 }; setHour(5); ScrollTrigger.create({ trigger: day, start: 'top top', end: 'bottom bottom', scrub: .4, onUpdate: s => { o.h = 5 + s.progress * 24; setHour(o.h); }, onRefresh: s => setHour(5 + s.progress * 24) }); }
  }

  // ---------- Sticky-Storytelling ----------
  const story = $('.story');
  if (story) {
    const imgs = $$('.frame img', story), chaps = $$('.chap', story), cnt = $('.cnt', story), bar = $('.bar i', story);
    const set = i => { imgs.forEach((im, k) => im.classList.toggle('on', k === i)); chaps.forEach((c, k) => c.classList.toggle('on', k === i)); cnt.textContent = `${String(i + 1).padStart(2, '0')} / ${String(chaps.length).padStart(2, '0')}`; bar.style.width = ((i + 1) / chaps.length * 100) + '%'; };
    set(0);
    chaps.forEach((c, i) => ScrollTrigger.create({ trigger: c, start: () => mobile() ? 'top 62%' : 'top 55%', end: () => mobile() ? 'bottom 62%' : 'bottom 55%', onEnter: () => set(i), onEnterBack: () => set(i) }));
  }

  // ---------- Text-Marquee mit Fotos: Tempo folgt dem Scrollen ----------
  const mq = $('.mq .track');
  if (mq && !reduce) {
    const row = $('.row', mq); mq.appendChild(row.cloneNode(true)); mq.appendChild(row.cloneNode(true));
    $$('.row', mq).slice(1).forEach(r => r.setAttribute('aria-hidden', 'true'));
    let x = 0, vel = 0; const st = ScrollTrigger.create({ onUpdate: s => vel = s.getVelocity() });
    gsap.ticker.add((t, dt) => { const w = row.offsetWidth; const v = clamp(Math.abs(vel) / 1200, 0, 5); x -= (0.6 + v * 2.2) * (dt / 16.7); vel *= .95; if (x <= -w) x += w; mq.style.transform = `translate3d(${x}px,0,0)`; });
  }

  // ---------- Mini-Rechner (Richtwerte – siehe LAUNCH-CHECKLISTE) ----------
  const cArea = $('#cArea');
  if (cArea) {
    const cUse = $('#cUse'), cDir = $('#cDir'), cBat = $('#cBat');
    const M2 = 5, YIELD = 950, PRICE = .35, FEED = .0778, CO2 = .38; // m² je kWp, kWh je kWp·a (Region Aachen), €/kWh Netzstrom, Einspeisevergütung 2/2026, kg CO₂ je kWh
    const num = { kwp: 0, yr: 0, self: 0, save: 0, co2: 0 };
    const paint = () => { $('#oKwp').textContent = fmt(num.kwp, 1); $('#oYr').textContent = fmt(num.yr); $('#oSelf').textContent = fmt(num.self); $('#oSave').textContent = fmt(num.save); $('#oCo2').textContent = fmt(num.co2, 1); };
    const calc = () => {
      const a = clamp(+cArea.value || 0, 0, 400), u = clamp(+cUse.value || 0, 0, 30000), f = +$('[aria-pressed=true]', cDir).dataset.f, withBat = cBat.checked;
      const kwp = a / M2, yr = kwp * YIELD * f; const share = withBat ? .6 : .3; const self = Math.min(yr * share, u * (withBat ? .8 : .45)); const feed = yr - self;
      const t = { kwp, yr, self, save: self * PRICE + feed * FEED, co2: yr * CO2 / 1000 };
      $('#oPct').textContent = yr ? Math.round(self / yr * 100) + ' %' : '– %';
      if (reduce) { Object.assign(num, t); paint(); } else gsap.to(num, { ...t, duration: .7, ease: 'power3.out', overwrite: true, onUpdate: paint });
    };
    [cArea, cUse].forEach(el => el.addEventListener('input', calc)); cBat.addEventListener('change', calc);
    $$('button', cDir).forEach(b => b.addEventListener('click', () => { $$('button', cDir).forEach(x => x.setAttribute('aria-pressed', 'false')); b.setAttribute('aria-pressed', 'true'); calc(); }));
    calc();
  }

  // ---------- EEG-Hinweis: Tage bis 1.1.2027 ----------
  const dl = $('#daysLeft');
  if (dl) { const d = Math.max(0, Math.ceil((new Date('2027-01-01T00:00:00') - new Date()) / 864e5)); dl.textContent = fmt(d); }

  // ---------- Große Telefonnummer: Ziffern „wählen“ beim Hover ----------
  $$('.bigtel').forEach(a => { a.innerHTML = a.textContent.split('').map((c, i) => `<span style="--i:${i}">${c === ' ' ? '&nbsp;' : c}</span>`).join(''); });

  // ---------- FAQ: nur eins offen ----------
  $$('.q').forEach(d => d.addEventListener('toggle', () => { if (d.open) $$('.q[open]').forEach(o => { if (o !== d) o.open = false; }); ScrollTrigger.refresh(); }));

  // ---------- Karte erst per Klick (OpenStreetMap) ----------
  $$('[data-map]').forEach(btn => btn.addEventListener('click', () => {
    const m = $('#' + btn.dataset.map); const [lat, lon] = btn.dataset.pos.split(',').map(Number); const d = .01;
    m.innerHTML = `<iframe title="Karte: ${btn.dataset.title}" loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox=${lon - d * 1.6}%2C${lat - d}%2C${lon + d * 1.6}%2C${lat + d}&layer=mapnik&marker=${lat}%2C${lon}"></iframe>`;
  }));

  // ---------- Kontaktformular: Themen-Vorwahl per ?thema=, Prüfung vor dem Senden ----------
  const form = $('#contactForm');
  if (form) {
    const topics = $$('.topics button', form), sel = $('#thema');
    const setTopic = v => { topics.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.v === v))); if (sel) sel.value = v; };
    topics.forEach(b => b.addEventListener('click', () => setTopic(b.dataset.v)));
    const q = new URLSearchParams(location.search).get('thema'); if (q && topics.some(b => b.dataset.v === q)) setTopic(q);
    form.addEventListener('submit', e => {
      const err = $('.err', form); err.classList.remove('show');
      if (!form.checkValidity()) { e.preventDefault(); err.textContent = 'Bitte prüfen Sie die rot markierten Felder.'; err.classList.add('show'); form.reportValidity(); return; }
      $('button[type=submit]', form).textContent = 'Wird gesendet …';
    });
  }

  // ---------- Konfigurator mit Bild-Vorschau (Photovoltaik) ----------
  const cfg = $('.cfg');
  if (cfg) {
    const st = { roof: 'sattel', size: 10, mod: 'black', bat: 5, wb: 1 };
    const svg = $('.preview svg', cfg);
    $$('.seg button', cfg).forEach(b => b.addEventListener('click', () => { const g = b.closest('.seg'); $$('button', g).forEach(x => x.setAttribute('aria-pressed', 'false')); b.setAttribute('aria-pressed', 'true'); st[g.dataset.k] = isNaN(b.dataset.v) ? b.dataset.v : +b.dataset.v; draw(); }));
    const draw = () => {
      const mods = Math.round(st.size / .45); const color = st.mod === 'black' ? '#15171c' : '#1f3f8c', grid = st.mod === 'black' ? '#2a2d34' : '#5b7fc7';
      const cols = st.roof === 'flach' ? 6 : 6, rows = Math.ceil(mods / cols);
      let g = '';
      if (st.roof === 'sattel') { g += `<polygon points="60,220 250,90 440,220" fill="#c0392b"/><polygon points="60,220 250,90 440,220" fill="none" stroke="#8e2a20" stroke-width="3"/>`; for (let i = 0; i < mods; i++) { const r = Math.floor(i / cols), c = i % cols; const y = 130 + r * 26, w = 170 + r * 44, x0 = 250 - w / 2 + c * (w / cols) + 3; g += `<rect x="${x0}" y="${y}" width="${w / cols - 6}" height="22" fill="${color}" stroke="${grid}" stroke-width="1.5" rx="1"/>`; } }
      else if (st.roof === 'pult') { g += `<polygon points="60,190 440,110 440,220 60,220" fill="#c0392b"/>`; for (let i = 0; i < mods; i++) { const r = Math.floor(i / cols), c = i % cols; const x = 80 + c * 56, y = 176 - c * 11.8 + r * 24; g += `<rect x="${x}" y="${y}" width="48" height="20" fill="${color}" stroke="${grid}" stroke-width="1.5" transform="skewY(-11.8) translate(0, ${x * .21})"/>`; } }
      else { g += `<rect x="60" y="150" width="380" height="70" fill="#9aa0a6"/>`; for (let i = 0; i < mods; i++) { const r = Math.floor(i / cols), c = i % cols; g += `<polygon points="${80 + c * 58},${176 + r * 22} ${80 + c * 58 + 46},${176 + r * 22} ${80 + c * 58 + 40},${166 + r * 22} ${80 + c * 58 - 6},${166 + r * 22}" fill="${color}" stroke="${grid}" stroke-width="1.5"/>`; } }
      g += `<rect x="90" y="220" width="320" height="150" fill="#f1e6d2"/><rect x="130" y="250" width="50" height="60" fill="#8fb8e8"/><rect x="225" y="250" width="50" height="60" fill="#8fb8e8"/><rect x="320" y="250" width="50" height="60" fill="#8fb8e8"/><rect x="230" y="320" width="40" height="50" fill="#6b4a2e"/>`;
      g += `<rect x="60" y="370" width="380" height="8" fill="#1d1d1f"/>`;
      // Wechselrichter
      g += `<rect x="100" y="330" width="26" height="30" fill="#e5e5ea" stroke="#1d1d1f" stroke-width="1.5"/><text x="113" y="350" font-size="8" text-anchor="middle" font-weight="700" fill="#1d1d1f">WR</text>`;
      if (st.bat) { const h = st.bat === 5 ? 34 : 50; g += `<rect x="140" y="${362 - h}" width="34" height="${h}" fill="#1d1d1f" rx="3"/><rect x="146" y="${368 - h}" width="22" height="${h - 12}" fill="#ffdf5b" rx="2" opacity=".9"/><text x="157" y="${356}" font-size="7" text-anchor="middle" font-weight="700" fill="#1d1d1f">${st.bat} kWh</text>`; }
      if (st.wb) { g += `<rect x="452" y="290" width="18" height="30" rx="6" fill="#1d1d1f"/><rect x="456" y="296" width="10" height="8" fill="#ffdf5b"/><path d="M470 300 q 30 0 30 40" fill="none" stroke="#1d1d1f" stroke-width="3"/><rect x="470" y="335" width="90" height="34" rx="12" fill="#ba0600"/><rect x="488" y="322" width="52" height="20" rx="8" fill="#ba0600"/><circle cx="490" cy="371" r="9" fill="#1d1d1f"/><circle cx="542" cy="371" r="9" fill="#1d1d1f"/>`; }
      if (st.bat || st.wb) g += `<path class="dash" d="M126 345 L140 345" stroke="#ba0600" stroke-width="2"/>`;
      svg.innerHTML = `<rect width="600" height="400" fill="#f5f5f7" rx="10"/><circle cx="520" cy="70" r="34" fill="#ffdf5b"/>` + g;
      const yr = st.size * 950; const share = st.bat ? (st.wb ? .7 : .6) : (st.wb ? .4 : .3);
      $('#kMods').textContent = mods + ' Module'; $('#kKwp').textContent = fmt(st.size, 1) + ' kWp'; $('#kYr').textContent = fmt(yr) + ' kWh/Jahr'; $('#kShare').textContent = Math.round(share * 100) + ' %';
      $('#kParts').innerHTML = `<b>${mods} × Heckert ZEUS ${st.mod === 'black' ? 'Full Black' : 'Glas-Glas'} (~450 Wp)</b> · Wagner TRIC ${st.roof === 'flach' ? 'Flachdach-Aufständerung' : 'Aufdach-System'} · SMA Wechselrichter${st.bat ? ` · SMA Speicher ${st.bat} kWh mit Notstromfunktion` : ''}${st.wb ? ' · Zappy Wallbox 11 kW inkl. Anmeldung beim Netzbetreiber' : ''}`;
      $('#kLink').href = `kontakt.html?thema=photovoltaik&konfig=${encodeURIComponent(`${st.roof}, ${st.size} kWp, ${st.mod}, Speicher ${st.bat} kWh, Wallbox ${st.wb ? 'ja' : 'nein'}`)}`;
    };
    draw();
  }

  // ---------- Checkliste zum Abhaken mit Fortschritt (Wallbox) ----------
  const chk = $('.chk');
  if (chk) {
    const boxes = $$('input[type=checkbox]', chk), fg = $('.ring .fg', chk), pct = $('.ring b', chk), txt = $('.res p', chk);
    const msgs = ['Los geht’s: Haken Sie ab, was bei Ihnen schon geklärt ist.', 'Guter Anfang – die restlichen Punkte klären wir beim Vor-Ort-Termin.', 'Fast startklar. Die offenen Punkte übernehmen wir für Sie.', 'Alles geklärt – Ihre Wallbox kann geplant und angemeldet werden.'];
    const upd = () => { const n = boxes.filter(b => b.checked).length, p = n / boxes.length; fg.style.strokeDashoffset = 1 - p; pct.textContent = Math.round(p * 100) + ' %'; txt.textContent = msgs[p === 0 ? 0 : p < .5 ? 1 : p < 1 ? 2 : 3]; };
    boxes.forEach(b => b.addEventListener('change', upd)); upd();
  }

  // ---------- Planer: Startzeitpunkt wählen → Phasen mit Terminen (Service & Anmeldung) ----------
  const plan = $('.plan2');
  if (plan) {
    const W = 7 * 864e5, deadline = new Date(2027, 0, 1);
    // Phasen in Wochen (Richtwerte, siehe LAUNCH-CHECKLISTE)
    const PH = [['Beratung vor Ort', 1, 'Dach, Zählerschrank, Ziele – kostenlos, durch den Elektromeister'], ['Angebot & Planung', 2, 'Belegungsplan, Komponenten, Speicher- und Wallbox-Option'], ['Netzbetreiber-Anmeldung', 6, 'Wir melden an – die Bearbeitungszeit bestimmt der Netzbetreiber'], ['Montage', 1, 'Dachhaken, Schienen, Module, Verkabelung – meist ein Tag'], ['Zähler & Inbetriebnahme', 3, 'Zählerwechsel, Messung, Einweisung, Monitoring'], ['Marktstammdatenregister', 4, 'Registrierung innerhalb eines Monats nach Inbetriebnahme']];
    const list = $('.phases', plan), res = $('.result', plan), btns = $$('.starts button', plan);
    const dstr = d => d.toLocaleDateString('de-DE', { day: '2-digit', month: 'short', year: 'numeric' });
    const dshort = d => d.toLocaleDateString('de-DE', { day: '2-digit', month: 'short' });
    btns.forEach(b => { if (+b.dataset.w) $('span', b).textContent = 'ab ' + dshort(new Date(Date.now() + b.dataset.w * W)); });
    const render = w => {
      let t = Date.now() + w * W; let html = ''; let placed = false; let ibn;
      PH.forEach(([name, wk, txt], i) => {
        const s = new Date(t), e = new Date(t + wk * W); t = e.getTime();
        if (i === 5) ibn = s; // Inbetriebnahme = Start der Registrierungsphase
        if (!placed && s >= deadline) { html += `<li class="deadline" aria-label="Stichtag 1. Januar 2027">Stichtag 1.1.2027</li>`; placed = true; }
        html += `<li class="phase${s >= deadline ? ' after' : ''}"><span class="n">${i + 1}</span><div><b>${name}</b><small>${txt}</small></div><span class="d">${dshort(s)} – ${dshort(e)}<em>${wk} Woche${wk > 1 ? 'n' : ''}</em></span></li>`;
      });
      if (!placed) html += `<li class="deadline">Stichtag 1.1.2027 – Inbetriebnahme liegt davor</li>`;
      list.innerHTML = html;
      const ok = ibn < deadline; res.classList.toggle('late', !ok);
      $('.date', res).textContent = dstr(ibn);
      $('.verdict', res).textContent = ok ? `Das liegt vor dem 1.1.2027 – Ihre Anlage könnte noch die feste Einspeisevergütung nach EEG 2023 erhalten (aktuell 7,78 ct/kWh, 20 Jahre). Puffer: ${Math.floor((deadline - ibn) / 864e5)} Tage.` : `Das liegt nach dem 1.1.2027 – dann greift voraussichtlich das EEG 2027 mit Übergangsvergütung und späterer Direktvermarktung. Je früher wir starten, desto besser.`;
    };
    btns.forEach(b => b.addEventListener('click', () => { btns.forEach(x => x.setAttribute('aria-pressed', 'false')); b.setAttribute('aria-pressed', 'true'); render(+b.dataset.w); }));
    render(0);
  }

  // ---------- Referenzkarte mit klickbaren Punkten (Über uns) ----------
  const rmap = $('.rmap');
  if (rmap) {
    const refs = JSON.parse($('#refData').textContent);
    const svg = $('svg', rmap), info = $('.info', rmap), list = $('.list', rmap);
    const X = lon => (lon - 5.95) / 1.4 * 800, Y = lat => (51.4 - lat) / .85 * 560;
    let g = `<rect class="land" x="0" y="0" width="800" height="560" rx="8"/>`;
    // grobe Orientierung: Rhein/Grenze als Linien
    g += `<path d="M 30 120 Q 90 180 60 300 T 40 540" fill="none" stroke="rgba(255,255,255,.12)" stroke-width="2" stroke-dasharray="6 6"/><text class="lbl" x="48" y="110">NL / BE</text>`;
    g += `<path d="M 620 0 Q 640 200 700 300 T 780 560" fill="none" stroke="rgba(120,170,255,.35)" stroke-width="4"/><text class="lbl" x="700" y="380">Rhein</text>`;
    refs.forEach((r, i) => { const x = X(r.lon), y = Y(r.lat); g += `<g class="pt${r.home ? ' home' : ''}" data-i="${i}" tabindex="0" role="button" aria-label="${r.ort}: ${r.titel}"><circle cx="${x}" cy="${y}" r="7"/><text x="${x + 12}" y="${y + 4}">${r.ort}</text></g>`; });
    svg.innerHTML = g;
    const show = i => { const r = refs[i]; $$('.pt', svg).forEach(p => p.classList.toggle('on', +p.dataset.i === i)); $$('button', list).forEach(b => b.classList.toggle('on', +b.dataset.i === i)); $('.pic', info).innerHTML = r.img ? `<img src="img/${r.img}.webp" alt="${r.alt || r.titel}" width="800" height="600" loading="lazy">` : ''; $('h3', info).textContent = r.titel; $('p', info).textContent = r.text; $('.kv', info).innerHTML = [r.ort, r.kwp && r.kwp + ' kWp', r.mod && r.mod + ' Module', r.jahr].filter(Boolean).map(v => `<span>${v}</span>`).join(''); };
    list.innerHTML = refs.map((r, i) => `<button data-i="${i}">${r.ort}</button>`).join('');
    $$('.pt', svg).forEach(p => { p.addEventListener('click', () => show(+p.dataset.i)); p.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); show(+p.dataset.i); } }); });
    $$('button', list).forEach(b => b.addEventListener('click', () => show(+b.dataset.i)));
    show(0);
  }

  // Nach dem Laden aller Bilder Trigger neu berechnen
  addEventListener('load', () => ScrollTrigger.refresh());
})();
