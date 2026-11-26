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
