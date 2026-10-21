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

  /* Background motion: retain poster-first mobile and reduced-motion behaviour. */
  var hero = document.querySelector('.hero');
  var video = hero && hero.querySelector('video');
  if (video) {
    var saveData = navigator.connection && navigator.connection.saveData;
    var userPaused = reduceMotion.matches || !!saveData || window.matchMedia('(max-width: 760px)').matches;
    var inView = true;
    var loaded = false;
    function loadVideo() {
      if (loaded) return;
      video.querySelectorAll('source[data-src]').forEach(function (source) { source.src = source.dataset.src; });
      loaded = true;
      video.load();
    }
    function playWhenAllowed() {
      if (userPaused || !inView || document.hidden) return;
      loadVideo();
      video.muted = true;
      var playing = video.play();
      if (playing && playing.catch) playing.catch(function () {});
    }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        inView = entries[0].isIntersecting;
        if (inView) playWhenAllowed(); else video.pause();
      }, { threshold: 0.01 }).observe(hero);
    }
    document.addEventListener('visibilitychange', function () {
      document.body.classList.toggle('paused', document.hidden);
      if (document.hidden) video.pause(); else playWhenAllowed();
    });
    if (reduceMotion.addEventListener) reduceMotion.addEventListener('change', function (event) {
      if (event.matches) { userPaused = true; video.pause(); }
    });
    playWhenAllowed();
  }

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
