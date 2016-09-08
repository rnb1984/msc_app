
var pizzaApp = angular.module('pizzaApp',[])
    .config(['$httpProvider', function($httpProvider) {
            console.log('got here')
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        }]);

// Controller for pizzas
pizzaApp.controller('pizzaController', function ($scope, $http ) {
    var  requp = {
         method: 'POST',
         url: '/userdetails/',
         headers: {
          'Content-Type': undefined
         },
         data: { allergies: 3, diet:5 }
    }
  
    $scope.new_userpro= '';
    $scope.userpro=[];
    var pizzadata = $http.get("/pizzas/"),
    ingredientdata = $http.get("/ingredients/"),
    userprodata = $http.get("/userdetails/");
    //userprodata = $http(requp);
    
    pizzadata.then(function (response) {
      $scope.pizzas = response.data;
      });
    
    ingredientdata.then(function (response) {
      $scope.ingredients = response.data;
      });
      
    userprodata.then(function (response) {
      $scope.userpro = response.data;
      console.log(response.data);
     });
     
     $scope.add = function(event){
         $http.post("/userdetails/",{dob: '1998-08-08' , gender:'M',  allergies:$scope.new_userpro,  diet: $scope.new_userpro, slug: $scope.new_userpro }).success(function(data){ 
           $scope.new_userpro = '';
           console.log('data');
           console.log(data);
            $scope.userpro.push(data);
           console.log('userpro is');
           console.log($scope.userpro);
         });
     };
     
     // todo
     $scope.that = function(item){
         
         $scope.userpro[item]['allergies'] = 300;
         var data = {id:$scope.userpro[item]['id'], dob: $scope.userpro[item]['dob'] , gender: $scope.userpro[item]['gender'],  allergies: $scope.userpro[item]['allergies'],  diet: $scope.userpro[item]['diet'], slug: $scope.userpro[item]['slug'] };
         var pk = $scope.userpro[item]['id'];
         $http.put("/userdetails/"+pk+"/",data).success(function(data){ 
           console.log(data);
         });
     };
     
     // todo
     $scope.the = function(item){
         console.log(item);
         
         $scope.userpro[item]['allergies'] = 0;
         var data = {id:$scope.userpro[item]['id'], dob: $scope.userpro[item]['dob'] , gender: $scope.userpro[item]['gender'],  allergies: $scope.userpro[item]['allergies'],  diet: $scope.userpro[item]['diet'], slug: $scope.userpro[item]['slug'] };
         var pk = $scope.userpro[item]['id'];
         $http.put("/userdetails/"+pk+"/",data).success(function(data){ 
           console.log(data);
         });
     };
     
});

