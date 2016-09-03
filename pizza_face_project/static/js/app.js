
var pizzaApp = angular.module('pizzaApp',[]);

// Define the `ComListController` controller on the `comApp` module
pizzaApp.controller('pizzaController', function SectionListController($scope, $http) {
    
    $http.get("https://pizza-face-site-robertburry.c9users.io/pizzas/?format=json").then(function (response) {
      console.log(response.data);
      $scope.pizzas = response.data;
    
  });
});
