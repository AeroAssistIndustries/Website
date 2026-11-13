(function () {
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
      var href = 'mailto:hello@karlasagency.com?subject=' + encodeURIComponent('Free audit request: ' + biz) + '&body=' + encodeURIComponent(lines.join('\n'));
      msg.innerHTML = 'Your request is ready. <a href="' + href + '">Open it in your email app</a> to send it, or email hello@karlasagency.com directly.';
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
