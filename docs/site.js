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
  var mb = document.querySelector('.menu-btn'), nl = document.getElementById('navlist');
  if (mb && nl) mb.addEventListener('click', function () {
    var open = nl.classList.toggle('open');
    mb.setAttribute('aria-expanded', String(open));
  });

  // Audit forms: build an email draft (the page itself has nowhere to send a form)
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
      var lines = [];
      Array.prototype.forEach.call(f.elements, function (el) {
        if (!el.name || el.type === 'submit') return;
        if (el.type === 'checkbox') { if (el.checked) lines.push(el.name + ': yes'); return; }
        if (el.value.trim()) lines.push((el.dataset.label || el.name) + ': ' + el.value.trim());
      });
      var href = 'mailto:hello@karladigital.com?subject=' + encodeURIComponent('Free audit request: ' + biz) + '&body=' + encodeURIComponent(lines.join('\n'));
      msg.innerHTML = 'Your request is ready. <a href="' + href + '">Open it in your email app</a> to send it, or email hello@karladigital.com directly.';
      msg.classList.add('show');
    });
  });

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
  function remember(text) { try { sessionStorage.setItem('ka-plan', text); } catch (e) {} }
  var dataEl = document.getElementById('plans-data');
  var PD = dataEl ? JSON.parse(dataEl.textContent) : null;
  document.querySelectorAll('[data-pick]').forEach(function (a) {
    a.addEventListener('click', function () {
      var bits = a.dataset.pick.split(':');
      var name = PD ? PD.plans.filter(function (p) { return p.id === bits[0]; })[0].name : bits[0];
      remember(name + ' (' + bits[1] + ')');
    });
  });

  // ---------- Plan builder ----------
  var bld = document.getElementById('builder');
  if (bld && PD) {
    var fmt = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };
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
      var bundlePct = picked.length >= 3 ? PD.bundle['3'] : picked.length === 2 ? PD.bundle['2'] : 0;
      var foundPct = fc && fc.checked ? PD.founding : 0;
      var pct = Math.max(bundlePct, foundPct);
      var html = picked.map(function (x) { return '<div><span>' + x.name + ' · ' + x.lvl + '</span><span>' + fmt(x.price) + '</span></div>'; }).join('');
      if (!picked.length) html = '<div><span>Tick a service to start.</span></div>';
      if (pct && picked.length) html += '<div class="save"><span>' + (pct === foundPct && foundPct >= bundlePct ? 'Founding client' : 'Bundle') + ' savings (' + pct + '%)</span><span>−' + fmt(sub * pct / 100) + '</span></div>';
      lines.innerHTML = html;
      totalEl.textContent = fmt(sub * (1 - pct / 100));
      noteEl.textContent = picked.length < 2 ? 'Add a second service to save 10%, or three or more to save 15%.' : picked.length === 2 ? 'Add one more service to save 15%.' : 'You are getting the best bundle rate.';
      if (foundPct) noteEl.textContent += ' The founding rate lasts 6 months and doesn’t stack with bundle savings.';
      var summary = picked.map(function (x) { return x.name + ' (' + x.lvl + ')'; }).join(', ');
      bld.dataset.summary = summary ? summary + ', about ' + totalEl.textContent + '/month' : '';
    }
    bld.addEventListener('change', calc);
    bld.querySelectorAll('.segs').forEach(function (sg) {
      sg.addEventListener('click', function () { var cb = sg.closest('.b-row').querySelector('input[type=checkbox]'); if (!cb.checked) { cb.checked = true; } setTimeout(calc, 0); });
    });
    var go = bld.querySelector('.go');
    if (go) go.addEventListener('click', function () { if (bld.dataset.summary) remember(bld.dataset.summary); });
    calc();
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
        verEl.innerHTML = '<div><b>' + msg[0] + '</b><p>' + msg[1] + ' <a href="' + full + '" style="color:#fff">See Google’s full report</a>.</p></div><a class="btn" href="contact.html#top" id="speedCta">Get my free audit</a>';
        var webF = document.getElementById('c-web'); if (webF && !webF.value) webF.value = url;
        out.hidden = false; st.className = 'speed-status'; st.textContent = 'Results for ' + url + ' (mobile).';
        var cta = document.getElementById('speedCta'); if (cta) cta.addEventListener('click', function (ev) { var f = document.querySelector('.audit-form'); if (f) { ev.preventDefault(); f.scrollIntoView({ behavior: 'smooth' }); var n = document.getElementById('c-name'); if (n) n.focus({ preventScroll: true }); } });
      }).catch(function () {
        st.className = 'speed-status'; st.textContent = 'Google’s live test is busy right now, so here’s the next best thing.';
        ringsEl.innerHTML = ''; metEl.innerHTML = '';
        verEl.innerHTML = '<div><b>Run the full test on Google’s site.</b><p>It takes about 30 seconds and checks the same four scores. Then send me your address and I’ll walk you through what to fix first.</p></div><div class="speed-acts"><a class="btn" href="' + full + '" target="_blank" rel="noopener">Open Google’s test</a><a class="btn ghost-w" href="contact.html#top" id="speedCta">Get my free audit</a></div>';
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
