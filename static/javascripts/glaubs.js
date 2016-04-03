(function () {
  'use strict';

  angular
    .module('glaubs', [
      'glaubs.config',
      'glaubs.routes',
      'glaubs.municipalities'
    ])
    .run(run);

  angular
    .module('glaubs.config', []);

  angular
    .module('glaubs.municipalities', []);

  angular
    .module('glaubs.routes', ['ngRoute']);


  /**
  * @name run
  * @desc Update xsrf $http headers to align with Django's defaults
  */
  function run($http) {
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';
  }

})();

