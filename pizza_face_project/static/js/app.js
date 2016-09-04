
var pizzaApp = angular.module('pizzaApp',[]);



// Controller for pizzas
pizzaApp.controller('pizzaController', function ($scope, $http) {
    var pizzadata = $http.get("https://pizza-face-site-robertburry.c9users.io/pizzas/?format=json"),
    ingredientdata = $http.get("https://pizza-face-site-robertburry.c9users.io/ingredients/?format=json");
    
    pizzadata.then(function (response) {
      console.log(response.data);
      $scope.pizzas = response.data;
      });
    
    ingredientdata.then(function (response) {
      console.log('got here');
      console.log(response.data);
      $scope.ingredients = response.data;
      });
});