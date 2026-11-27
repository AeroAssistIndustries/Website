(function () {
  // Scroll reveal (content stays visible if anything fails)
  var rv = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    rv.forEach(function (el) { io.observe(el); });
  } else { rv.forEach(function (el) { el.classList.add('in'); }); }

  // Mobile menu
  var mb = document.querySelector('.menu-btn'), nl = document.getElementById('navlist'), navEl = document.querySelector('.nav');
  function setMenu(open) {
    if (!mb || !nl) return;
    if (navEl) document.documentElement.style.setProperty('--navh', navEl.getBoundingClientRect().height + 'px');
    nl.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
    mb.setAttribute('aria-expanded', String(open));
    var t = mb.querySelector('.mb-t'); if (t) t.textContent = open ? 'Close' : 'Menu';
  }
  if (mb && nl) {
    mb.addEventListener('click', function () { setMenu(!nl.classList.contains('open')); });
    nl.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        if (nl.classList.contains('open')) { setMenu(false); mb.focus(); }
        document.querySelectorAll('.has-sub.show').forEach(function (li) { li.classList.remove('show'); li.querySelector('.sub-btn').setAttribute('aria-expanded', 'false'); });
      }
    });
    window.addEventListener('resize', function () { if (window.innerWidth > 960 && nl.classList.contains('open')) setMenu(false); });
  }
  // Services dropdown (click/tap toggle; hover handled in CSS on desktop)
  document.querySelectorAll('.has-sub .sub-btn').forEach(function (b) {
    b.addEventListener('click', function (e) {
      e.stopPropagation();
      var li = b.parentNode, open = !li.classList.contains('show');
      li.classList.toggle('show', open); b.setAttribute('aria-expanded', String(open));
    });
  });
  document.addEventListener('click', function (e) {
    if (window.innerWidth > 960 && !e.target.closest('.has-sub')) document.querySelectorAll('.has-sub.show').forEach(function (li) { li.classList.remove('show'); li.querySelector('.sub-btn').setAttribute('aria-expanded', 'false'); });
  });

  // Audit forms. With FORM_ENDPOINT set (a form service or Cloudflare Worker URL) requests are sent
  // straight to the inbox; without it, or if sending fails, the visitor gets a ready-made email draft.
  var FORM_ENDPOINT = '', EMAIL = 'hello@digitalmondo.com';
  document.querySelectorAll('form.audit-form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = f.querySelector('.form-msg');
      var val = function (n) { var el = f.elements[n]; return el ? el.value.trim() : ''; };
      var name = val('name'), biz = val('business'), email = val('email');
      if (!name || !biz || !/^\S+@\S+\.\S+$/.test(email)) {
        msg.textContent = 'Please add your name, business name and a valid email.';
        msg.classList.add('show'); return;
      }
      if (f.elements._gotcha && f.elements._gotcha.value) return; // a bot filled the hidden field
      var lines = [];
      Array.prototype.forEach.call(f.elements, function (el) {
        if (!el.name || el.type === 'submit' || el.name === '_gotcha') return;
        if (el.type === 'checkbox') { if (el.checked) lines.push(el.name + ': yes'); return; }
        if (el.type === 'radio' && !el.checked) return;
        if (el.value.trim()) lines.push((el.dataset.label || el.name) + ': ' + el.value.trim());
      });
      var href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent((f.dataset.subject || 'Free audit request') + ': ' + biz) + '&body=' + encodeURIComponent(lines.join('\n'));
      var draft = function (lead) {
        msg.innerHTML = lead + ' <a href="' + href + '">Open it in your email app</a> to send it, or email ' + EMAIL + ' directly.';
        msg.classList.add('show');
      };
      if (!FORM_ENDPOINT || !window.fetch) { draft('Your request is ready.'); return; }
      var btn = f.querySelector('[type=submit]'), label = btn.textContent;
      btn.disabled = true; btn.textContent = 'Sending…';
      var data = new FormData(f); data.append('_subject', (f.dataset.subject || 'Free audit request') + ': ' + biz); data.append('summary', lines.join('\n'));
      fetch(FORM_ENDPOINT, { method: 'POST', body: data, headers: { Accept: 'application/json' } }).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        f.reset(); f.dispatchEvent(new Event('change')); msg.textContent = 'Thank you, ' + name + '! ' + (f.dataset.subject ? 'I\u2019ll confirm your call by email within one business day.' : 'Your request is in. I\u2019ll reply within one business day.'); msg.classList.add('show');
        try { sessionStorage.removeItem('ka-plan'); } catch (e) {}
      }).catch(function () { draft('That didn\u2019t go through, but your request is ready.'); })
        .then(function () { btn.disabled = false; btn.textContent = label; });
    });
  });

  // ---------- Newsletter signup ----------
  document.querySelectorAll('form.news-form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = f.querySelector('.news-msg'), email = f.elements.email.value.trim();
      if (!/^\S+@\S+\.\S+$/.test(email)) { msg.textContent = 'Please enter a valid email address.'; f.elements.email.focus(); return; }
      if (f.elements._gotcha && f.elements._gotcha.value) return;
      var href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent('Newsletter signup') + '&body=' + encodeURIComponent('Please add me to the Digital Mondo monthly note: ' + email);
      var draft = function (lead) { msg.innerHTML = lead + ' <a href="' + href + '">Open it in your email app</a> to send it.'; };
      if (!FORM_ENDPOINT || !window.fetch) { draft('Almost there.'); return; }
      var btn = f.querySelector('[type=submit]'); btn.disabled = true;
      var data = new FormData(f); data.append('_subject', 'Newsletter signup'); data.append('summary', 'Newsletter signup: ' + email);
      fetch(FORM_ENDPOINT, { method: 'POST', body: data, headers: { Accept: 'application/json' } }).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        f.reset(); msg.textContent = 'You’re on the list. Thank you!';
      }).catch(function () { draft('That didn’t go through.'); }).then(function () { btn.disabled = false; });
    });
  });

  // ---------- Blog: topic filter and search ----------
  var bGrid = document.getElementById('blogGrid');
  if (bGrid) {
    var chipsB = Array.prototype.slice.call(document.querySelectorAll('.b-chip')), q = document.getElementById('blogQ');
    var cards = Array.prototype.slice.call(document.querySelectorAll('.b-post[data-cat]'));
    var feat = document.querySelector('.b-featwrap'), count = document.getElementById('blogCount'), empty = document.getElementById('blogEmpty');
    var cat = 'all';
    var apply = function () {
      var term = q.value.trim().toLowerCase(), n = 0;
      cards.forEach(function (c) {
        var ok = (cat === 'all' || c.dataset.cat === cat) && (!term || c.dataset.text.indexOf(term) > -1);
        if (c.parentNode === feat) feat.hidden = !ok; else c.hidden = !ok;
        if (ok) n++;
      });
      count.textContent = n === 1 ? '1 post' : n + ' posts';
      empty.hidden = n > 0;
    };
    chipsB.forEach(function (b) {
      b.addEventListener('click', function () {
        cat = b.dataset.cat;
        chipsB.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
        apply();
      });
    });
    q.addEventListener('input', apply);
    var want = new URLSearchParams(location.search).get('cat');
    if (want) chipsB.forEach(function (b) { if (b.dataset.cat === want) b.click(); });
  }

  // Social examples filter
  var fb = document.querySelectorAll('.filters button');
  if (fb.length) {
    var secs = document.querySelectorAll('.brand');
    fb.forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.dataset.f;
        fb.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
        secs.forEach(function (s) { s.hidden = !(f === 'all' || s.dataset.ind === f); });
      });
    });
  }


  // ---------- Plans: service tabs ----------
  document.querySelectorAll('.plans').forEach(function (root) {
    var tabs = Array.prototype.slice.call(root.querySelectorAll('[role="tab"]'));
    function show(t) {
      tabs.forEach(function (x) {
        var on = x === t;
        x.setAttribute('aria-selected', String(on)); x.tabIndex = on ? 0 : -1;
        document.getElementById(x.getAttribute('aria-controls')).hidden = !on;
      });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { show(t); });
      t.addEventListener('keydown', function (e) {
        var k = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!k) return;
        var n = tabs[(i + k + tabs.length) % tabs.length]; n.focus(); show(n); e.preventDefault();
      });
    });
    var want = location.hash.replace('#', '');
    var hit = tabs.filter(function (t) { return t.id === 'tab-' + want; })[0];
    if (hit) show(hit);
  });

  // Remember a chosen plan so the audit form can mention it
  var dataEl = document.getElementById('plans-data');
  var PD = dataEl ? JSON.parse(dataEl.textContent) : null;

  // ---------- Monthly / yearly billing ----------
  var YM = PD ? PD.yearMonths : 10, yearly = false, onBilling = [];
  try { yearly = sessionStorage.getItem('ka-bill') === 'y'; } catch (e) {}
  var money = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };
  var eq = function (m) { return Math.floor(m * YM / 12); };
  function paintPrices(root) {
    (root || document).querySelectorAll('[data-m]').forEach(function (el) { var m = +el.dataset.m; el.textContent = money(yearly ? eq(m) : m); });
  }
  function setBilling(y) {
    yearly = y;
    try { sessionStorage.setItem('ka-bill', y ? 'y' : 'm'); } catch (e) {}
    document.documentElement.classList.toggle('yearly', y);
    document.querySelectorAll('.billing button').forEach(function (b) { b.setAttribute('aria-pressed', (b.dataset.bill === 'y') === y); });
    paintPrices();
    onBilling.forEach(function (f) { f(); });
  }
  document.querySelectorAll('.billing button').forEach(function (b) {
    b.addEventListener('click', function () { setBilling(b.dataset.bill === 'y'); });
  });

  function remember(text) { if (yearly) text += ', paid yearly (2 months free)'; try { sessionStorage.setItem('ka-plan', text); } catch (e) {} }
  document.querySelectorAll('[data-pick],[data-label]').forEach(function (a) {
    a.addEventListener('click', function () {
      if (a.dataset.label) { remember(a.dataset.label); return; }
      var bits = a.dataset.pick.split(':');
      var name = PD ? PD.plans.filter(function (p) { return p.id === bits[0]; })[0].name : bits[0];
      remember(name + ' (' + bits[1] + ')');
    });
  });

  // ---------- À la carte / Combos switch ----------
  var modes = document.querySelector('.pk-modes');
  if (modes) {
    var mBtns = [].slice.call(modes.querySelectorAll('[role=tab]'));
    var showMode = function (btn, focus) {
      mBtns.forEach(function (b) {
        var on = b === btn; b.setAttribute('aria-selected', on); b.tabIndex = on ? 0 : -1;
        document.getElementById(b.getAttribute('aria-controls')).hidden = !on;
      });
      if (focus) btn.focus();
    };
    mBtns.forEach(function (b, i) {
      b.addEventListener('click', function () { showMode(b); });
      b.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); showMode(mBtns[(i + (e.key === 'ArrowRight' ? 1 : mBtns.length - 1)) % mBtns.length], true); }
      });
    });
    if (/^#(combos|complete)$/.test(location.hash)) { showMode(mBtns[1]); var pk = document.getElementById('packages'); if (pk) setTimeout(function () { pk.scrollIntoView(); }, 50); }
    document.querySelectorAll('a[href$="#combos"]').forEach(function (a) {
      if (a.pathname === location.pathname) a.addEventListener('click', function (e) { e.preventDefault(); showMode(mBtns[1]); document.getElementById('packages').scrollIntoView({ behavior: 'smooth' }); });
    });
  }
  var lsw = document.querySelector('.lvl-switch');
  if (lsw) {
    lsw.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      var i = b.dataset.lvl, tier = b.textContent;
      lsw.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      document.querySelectorAll('.combo-card').forEach(function (c) {
        var pm = +c.dataset['p' + i];
        c.querySelector('.cc-price b').dataset.m = pm;
        c.querySelector('.cc-price s').dataset.m = c.dataset['f' + i];
        var bl = c.querySelector('.billed'); if (bl) bl.textContent = 'Billed ' + money(pm * YM) + ' a year · 2 months free';
        c.querySelector('.cc-save').textContent = 'You save ' + c.dataset['s' + i] + ' a month';
        c.querySelector('.btn').dataset.label = c.dataset.name + ' (' + tier + '), ' + money(pm) + '/month';
        paintPrices(c);
        c.classList.remove('bump'); void c.offsetWidth; c.classList.add('bump');
      });
    });
  }

  // ---------- Plan builder ----------
  var bld = document.getElementById('builder');
  if (bld && PD) {
    var fmt = money;
    var lines = bld.querySelector('.lines'), totalEl = bld.querySelector('.total b'), noteEl = bld.querySelector('.note'), fc = bld.querySelector('#founding');
    function calc() {
      var picked = [], sub = 0;
      bld.querySelectorAll('.b-row').forEach(function (row) {
        var on = row.querySelector('input[type=checkbox]').checked;
        row.classList.toggle('on', on);
        if (!on) return;
        var id = row.dataset.service, plan = PD.plans.filter(function (p) { return p.id === id; })[0];
        var lvl = (row.querySelector('input[type=radio]:checked') || {}).value || 'Growth';
        var price = plan.prices[PD.tiers.indexOf(lvl)];
        picked.push({ name: plan.short, lvl: lvl, price: price }); sub += price;
      });
      var n = picked.length, bundlePct = n >= 2 ? PD.bundle[String(Math.min(n, 4))] : 0;
      var foundPct = fc && fc.checked && !yearly ? PD.founding : 0;
      if (fc) { fc.disabled = yearly; fc.closest('label').classList.toggle('off', yearly); }
      var pct = Math.max(bundlePct, foundPct);
      var html = picked.map(function (x) { return '<div><span>' + x.name + ' · ' + x.lvl + '</span><span>' + fmt(x.price) + '</span></div>'; }).join('');
      if (!picked.length) html = '<div><span>Tick a service to start.</span></div>';
      if (pct && picked.length) html += '<div class="save"><span>' + (pct === foundPct && foundPct >= bundlePct ? 'Founding client' : 'Combo') + ' savings (' + pct + '%)</span><span>−' + fmt(sub * pct / 100) + '</span></div>';
      lines.innerHTML = html;
      var total = pct ? Math.floor(sub * (100 - pct) / 100 / 5) * 5 : sub;
      if (pct && picked.length) lines.querySelector('.save span:last-child').textContent = '−' + fmt(sub - total);
      totalEl.textContent = fmt(yearly ? eq(total) : total);
      var billedEl = bld.querySelector('.total-billed');
      if (billedEl) billedEl.textContent = yearly && n ? 'Billed ' + fmt(total * YM) + ' a year · you save ' + fmt(total * (12 - YM)) : '';
      noteEl.textContent = n < 2 ? 'Add a second service to save 10%. Three save 15%, all four save 20%.' : n === 2 ? 'Add a third service to save 15%, or all four to save 20%.' : n === 3 ? 'Add the fourth service to save 20% on everything.' : 'You have the Complete Package rate: 20% off all four.';
      if (foundPct) noteEl.textContent += ' The founding rate lasts 6 months and doesn’t stack with bundle savings.';
      if (yearly) noteEl.textContent += ' Paying yearly gives you 2 months free on top of combo savings (the founding rate is for monthly plans).';
      var summary = picked.map(function (x) { return x.name + ' (' + x.lvl + ')'; }).join(', ');
      bld.dataset.summary = summary ? summary + ', about ' + fmt(total) + '/month' : '';
    }
    bld.addEventListener('change', calc);
    bld.querySelectorAll('.segs').forEach(function (sg) {
      sg.addEventListener('click', function () { var cb = sg.closest('.b-row').querySelector('input[type=checkbox]'); if (!cb.checked) { cb.checked = true; } setTimeout(calc, 0); });
    });
    onBilling.push(calc);
    // Restore a shared plan: pricing.html?plan=social-growth,seo-pro&billing=yearly&founding=1#builder
    try {
      var qs = new URLSearchParams(location.search), want = (qs.get('plan') || '').toLowerCase();
      if (want) {
        want.split(',').forEach(function (bit) {
          var kv = bit.split('-'), row = bld.querySelector('.b-row[data-service="' + kv[0] + '"]');
          if (!row) return;
          row.querySelector('input[type=checkbox]').checked = true;
          var lv = (kv[1] || '').charAt(0).toUpperCase() + (kv[1] || '').slice(1);
          var r = row.querySelector('input[type=radio][value="' + lv + '"]'); if (r) r.checked = true;
        });
        yearly = qs.get('billing') === 'yearly';
        if (qs.get('founding') === '1' && fc) fc.checked = true;
      }
    } catch (e) {}
    function planLink() {
      var bits = [];
      bld.querySelectorAll('.b-row').forEach(function (row) {
        if (!row.querySelector('input[type=checkbox]').checked) return;
        var lv = (row.querySelector('input[type=radio]:checked') || {}).value || 'Growth';
        bits.push(row.dataset.service + '-' + lv.toLowerCase());
      });
      if (!bits.length) return '';
      var q = '?plan=' + bits.join(',') + (yearly ? '&billing=yearly' : '') + (fc && fc.checked && !yearly ? '&founding=1' : '');
      return location.origin + location.pathname + q + '#builder';
    }
    var shareBtn = document.getElementById('bShare'), printBtn = document.getElementById('bPrint'), shareMsg = document.getElementById('bShareMsg');
    if (shareBtn) shareBtn.addEventListener('click', function () {
      var url = planLink();
      if (!url) { shareMsg.textContent = 'Tick at least one service first.'; return; }
      var shown = function () { shareMsg.textContent = 'Copy this link: ' + url; };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(function () { shareMsg.textContent = 'Link copied. Anyone who opens it sees this plan.'; }, shown);
      else shown();
    });
    if (printBtn) printBtn.addEventListener('click', function () {
      if (!planLink()) { shareMsg.textContent = 'Tick at least one service first.'; return; }
      var qd = document.getElementById('bQuoteDate'); if (qd) qd.textContent = 'Plan quote · ' + new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
      document.body.classList.add('print-quote'); window.print();
      setTimeout(function () { document.body.classList.remove('print-quote'); }, 500);
    });
    window.addEventListener('afterprint', function () { document.body.classList.remove('print-quote'); });
    var go = bld.querySelector('.go');
    if (go) go.addEventListener('click', function () { if (bld.dataset.summary) remember(bld.dataset.summary); });
    calc();
  }

  if (document.querySelector('[data-m]')) setBilling(yearly);

  // ---------- Guides: reading progress and copy link ----------
  var rp = document.querySelector('.read-progress i'), art = document.querySelector('.g-prose');
  if (rp && art) {
    var prog = function () { var r = art.getBoundingClientRect(), h = r.height - window.innerHeight * .6; var p = h > 0 ? Math.min(1, Math.max(0, -r.top / h)) : 1; rp.style.transform = 'scaleX(' + p + ')'; };
    window.addEventListener('scroll', prog, { passive: true }); prog();
  }
  document.querySelectorAll('.copy-link').forEach(function (b) {
    b.addEventListener('click', function () {
      var done = function () { var t = b.textContent; b.textContent = 'Link copied'; setTimeout(function () { b.textContent = t; }, 1800); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(b.dataset.url).then(done, function () { window.prompt('Copy this link:', b.dataset.url); });
      else window.prompt('Copy this link:', b.dataset.url);
    });
  });

  // ---------- Back to top ----------
  var tt = document.querySelector('.to-top');
  if (tt) {
    var onScroll = function () { tt.classList.toggle('show', window.scrollY > 1200); };
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
    tt.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); var m = document.getElementById('main'); if (m) { m.setAttribute('tabindex', '-1'); m.focus({ preventScroll: true }); } });
  }

  // ---------- Customer value calculator ----------
  var calcEl = document.getElementById('calc');
  if (calcEl) {
    var val = function (id) { var v = parseFloat(document.getElementById(id).value); return isFinite(v) && v > 0 ? v : 0; };
    var cash = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };
    var runCalc = function () {
      var spend = val('v-spend'), visits = val('v-visits'), years = val('v-years'), margin = Math.min(val('v-margin'), 100) / 100;
      var plan = +document.getElementById('v-plan').value;
      var rev = spend * visits * years, profit = rev * margin;
      document.getElementById('v-rev').textContent = cash(rev);
      document.getElementById('v-ltv').textContent = cash(profit);
      var need = profit ? plan / profit : 0, needEl = document.getElementById('v-need'), note = document.getElementById('v-note');
      needEl.textContent = !profit ? '–' : need < 1 ? 'Under 1' : (Math.round(need * 10) / 10).toString();
      if (!profit) { note.textContent = 'Fill in your numbers to see the result.'; return; }
      var every = Math.round(1 / need);
      note.textContent = need < 1
        ? 'One new customer every ' + (every > 1 ? every + ' months' : 'month') + ' would cover this plan. Everything beyond that is growth.'
        : 'About ' + Math.ceil(need) + ' new customer' + (Math.ceil(need) > 1 ? 's' : '') + ' a month would cover this plan, out of everyone who finds you on Google, social media and your website.';
    };
    calcEl.addEventListener('input', runCalc);
    calcEl.addEventListener('change', runCalc);
    runCalc();
  }

  // Prefill the audit form with a chosen plan
  var msgBox = document.getElementById('c-msg');
  if (msgBox) { try { var pl = sessionStorage.getItem('ka-plan'); if (pl && !msgBox.value) msgBox.value = 'Interested in: ' + pl; } catch (e) {} }


  // ---------- Website speed check (Google PageSpeed Insights) ----------
  // Optional: paste a free Google PageSpeed Insights API key here so the test never hits the shared daily limit.
  var PSI_KEY = '';
  var sf = document.getElementById('speedForm');
  if (sf) {
    var st = document.getElementById('speedStatus'), out = document.getElementById('speedOut');
    var ringsEl = document.getElementById('speedRings'), metEl = document.getElementById('speedMetrics'), verEl = document.getElementById('speedVerdict');
    var color = function (n) { return n >= 90 ? '#1a8f5a' : n >= 50 ? '#c77700' : '#c2412f'; };
    var ring = function (label, n) {
      var c = 2 * Math.PI * 40, off = c * (1 - n / 100);
      return '<div class="ring"><svg viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="40" fill="none" stroke="#e6e8e2" stroke-width="9"/><circle cx="50" cy="50" r="40" fill="none" stroke="' + color(n) + '" stroke-width="9" stroke-linecap="round" stroke-dasharray="' + c.toFixed(1) + '" stroke-dashoffset="' + off.toFixed(1) + '" transform="rotate(-90 50 50)"/><text x="50" y="58" text-anchor="middle" font-size="26" font-weight="800" fill="' + color(n) + '" font-family="Bricolage Grotesque, sans-serif">' + n + '</text></svg><b>' + label + '</b><small>' + (n >= 90 ? 'Good' : n >= 50 ? 'Needs work' : 'Poor') + '</small></div>';
    };
    sf.addEventListener('submit', function (e) {
      e.preventDefault();
      var raw = sf.elements.url.value.trim();
      if (!raw) { st.textContent = 'Enter your website address, like yourbusiness.com.'; return; }
      var url = /^https?:\/\//i.test(raw) ? raw : 'https://' + raw;
      try { new URL(url); } catch (err) { st.textContent = 'That doesn’t look like a web address. Try yourbusiness.com.'; return; }
      var btn = sf.querySelector('button'); btn.disabled = true; out.hidden = true;
      st.className = 'speed-status busy'; st.textContent = 'Testing ' + url + ' on a mobile connection…';
      var api = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?strategy=mobile&category=performance&category=accessibility&category=best-practices&category=seo&url=' + encodeURIComponent(url) + (PSI_KEY ? '&key=' + encodeURIComponent(PSI_KEY) : '');
      var full = 'https://pagespeed.web.dev/analysis?url=' + encodeURIComponent(url);
      fetch(api).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (d) {
        var cat = d.lighthouseResult.categories, au = d.lighthouseResult.audits;
        var sc = function (k) { return Math.round((cat[k] && cat[k].score || 0) * 100); };
        var perf = sc('performance');
        ringsEl.innerHTML = ring('Performance', perf) + ring('Accessibility', sc('accessibility')) + ring('Best practices', sc('best-practices')) + ring('SEO', sc('seo'));
        var m = function (k, label) { return au[k] ? '<div><b>' + au[k].displayValue + '</b><span>' + label + '</span></div>' : ''; };
        metEl.innerHTML = m('largest-contentful-paint', 'Main content shows') + m('first-contentful-paint', 'First thing appears') + m('total-blocking-time', 'Time frozen by scripts') + m('cumulative-layout-shift', 'Layout jumping (lower is better)');
        var msg = perf >= 90 ? ['Your site is fast.', 'Nice work. Speed isn’t holding you back, so the next wins are usually your Google profile and reviews.']
          : perf >= 50 ? ['Your site is a little slow on phones.', 'Most visitors are on mobile. A few fixes to images and scripts could keep more of them on your page long enough to call or book.']
          : ['Your site is losing mobile visitors.', 'Pages this slow on phones lose many visitors before they load. This is usually very fixable, and it’s one of the quickest wins I see.'];
        verEl.innerHTML = '<div><b>' + msg[0] + '</b><p>' + msg[1] + ' <a href="' + full + '" style="color:#fff">See Google’s full report</a>.</p></div><a class="btn" href="contact.html" id="speedCta">Get my free audit</a>';
        var webF = document.getElementById('c-web'); if (webF && !webF.value) webF.value = url;
        out.hidden = false; st.className = 'speed-status'; st.textContent = 'Results for ' + url + ' (mobile).';
        var cta = document.getElementById('speedCta'); if (cta) cta.addEventListener('click', function (ev) { var f = document.querySelector('.audit-form'); if (f) { ev.preventDefault(); f.scrollIntoView({ behavior: 'smooth' }); var n = document.getElementById('c-name'); if (n) n.focus({ preventScroll: true }); } });
      }).catch(function () {
        st.className = 'speed-status'; st.textContent = 'Google’s live test is busy right now, so here’s the next best thing.';
        ringsEl.innerHTML = ''; metEl.innerHTML = '';
        verEl.innerHTML = '<div><b>Run the full test on Google’s site.</b><p>It takes about 30 seconds and checks the same four scores. Then send me your address and I’ll walk you through what to fix first.</p></div><div class="speed-acts"><a class="btn" href="' + full + '" target="_blank" rel="noopener">Open Google’s test</a><a class="btn ghost-w" href="contact.html" id="speedCta">Get my free audit</a></div>';
        var webF2 = document.getElementById('c-web'); if (webF2 && !webF2.value) webF2.value = url;
        out.hidden = false;
        var cta2 = document.getElementById('speedCta'); if (cta2) cta2.addEventListener('click', function (ev) { var f = document.querySelector('.audit-form'); if (f) { ev.preventDefault(); f.scrollIntoView({ behavior: 'smooth' }); } });
      }).then(function () { btn.disabled = false; });
    });
  }

  // Google Business Profile checklist
  var cl = document.getElementById('gbpChecklist');
  if (cl) {
    var KEY = 'ka-gbp-checklist', saved = {};
    try { saved = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) {}
    var boxes = cl.querySelectorAll('input[type=checkbox]');
    var bar = document.getElementById('clBar'), num = document.getElementById('clNum'), verdict = document.getElementById('clVerdict');
    function update() {
      var done = 0, state = {};
      boxes.forEach(function (b) { if (b.checked) { done++; state[b.id] = 1; } });
      var pct = Math.round(done / boxes.length * 100);
      bar.style.width = pct + '%';
      num.textContent = done + ' of ' + boxes.length;
      verdict.textContent = pct === 100 ? 'Your profile is in great shape. Keep posting and replying every week.'
        : pct >= 70 ? 'Strong start. A few gaps are holding your profile back.'
        : pct >= 40 ? 'Halfway there. Filling the gaps below can make a real difference in local search.'
        : 'Lots of room to grow. These basics are the fastest wins in local search.';
      try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {}
    }
    boxes.forEach(function (b) { if (saved[b.id]) b.checked = true; b.addEventListener('change', update); });
    var reset = document.getElementById('clReset');
    if (reset) reset.addEventListener('click', function () { boxes.forEach(function (b) { b.checked = false; }); update(); });
    update();
  }
})();
