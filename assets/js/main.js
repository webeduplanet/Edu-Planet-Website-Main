/* EduPlanet Independent School — site behaviour
   Everything here is progressive: the site is complete and readable with JS off. */
(function () {
  'use strict';

  // Tells the head-script safety net that entrances are being driven, so it
  // leaves the .js class alone.
  window.__epReady = true;

  /* ---------------------------------------------------------- mobile nav */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        toggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('is-open');
        toggle.focus();
      }
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        toggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('is-open');
      }
    });
  }

  /* ------------------------------------------------------- header state */
  var header = document.querySelector('.header');
  var scrollCue = document.querySelector('.hero__scroll');
  if (header) {
    var scrolled = false;
    var onScroll = function () {
      var now = window.scrollY > 12;
      if (now !== scrolled) {            // write only on change
        scrolled = now;
        header.classList.toggle('is-scrolled', now);
      }
      // On short screens, let the cue enter view before dismissing it.
      if (scrollCue) {
        var cueEnd = scrollCue.parentElement.offsetTop + scrollCue.parentElement.offsetHeight;
        scrollCue.classList.toggle('is-dismissed', window.scrollY > Math.max(48, cueEnd - window.innerHeight + 48));
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ------------------------------------------------------------ reveals */
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var targets = document.querySelectorAll('.reveal, .stagger');

  if (!reduceMotion.matches && 'IntersectionObserver' in window && targets.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        el.classList.add('in');
        io.unobserve(el);
        if (el.classList.contains('stagger')) {
          window.setTimeout(function () { el.classList.add('done'); }, 1200);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    targets.forEach(function (el) { io.observe(el); });
  } else {
    targets.forEach(function (el) { el.classList.add('in', 'done'); });
  }

  /* --------------------------------------------------------- hero video
     Playback is started by the browser itself: the element carries `autoplay`
     and its sources in the markup, so it begins during page parse rather than
     waiting for this script. Everything here is a safety net around that. */
  var hero = document.querySelector('.hero');
  var video = hero && hero.querySelector('video');

  // Some browsers refuse muted autoplay regardless — iOS in Low Power Mode is
  // the common one. Rather than leave a silent still, offer the play.
  function offerPlayButton() {
    if (!hero || hero.querySelector('.hero__play') || !video.querySelector('source')) return;
    var host = hero.querySelector('.hero__inner .wrap') || hero;
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'hero__play';
    b.innerHTML =
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.4v13.2L19 12z"/></svg>' +
      '<span>Play video</span>';
    b.addEventListener('click', function () {
      video.muted = true;                       // a muted play is the one browsers allow
      var p = video.play();
      if (p && p.then) { p.then(function () { b.remove(); }).catch(function () {}); }
      else { b.remove(); }
    });
    host.appendChild(b);
  }

  if (video) {
    // Nudge it once, in case autoplay was deferred rather than refused.
    var kick = function () {
      if (!video.paused || !video.querySelector('source')) return;
      var p = video.play();
      if (p && p.catch) { p.catch(function () { if (video.paused) offerPlayButton(); }); }
    };
    if (video.readyState >= 2) { kick(); }
    video.addEventListener('loadeddata', kick, { once: true });
    window.addEventListener('load', kick, { once: true });

    // If it still has not started shortly after load, autoplay was refused.
    window.setTimeout(function () {
      if (video.paused && video.querySelector('source')) { offerPlayButton(); }
    }, 1800);

    // Don't keep decoding off-screen.
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!video.querySelector('source')) return;
          if (e.isIntersecting) { video.play().catch(function () {}); }
          else { video.pause(); }
        });
      }, { threshold: 0.01 }).observe(hero);
    }
  }

  /* --------------------------------------------------- pause on hidden tab */
  document.addEventListener('visibilitychange', function () {
    document.body.classList.toggle('paused', document.hidden);
    if (video && video.querySelector('source')) {
      if (document.hidden) { video.pause(); }
      else { video.play().catch(function () {}); }
    }
  });

  /* ------------------------------------------------------------- accordion */
  document.querySelectorAll('.faq__q').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      document.getElementById(btn.getAttribute('aria-controls')).hidden = open;
    });
  });

  /* ------------------------------------------------------------- footer */
  var year = document.getElementById('year');
  if (year) { year.textContent = String(new Date().getFullYear()); }
})();
