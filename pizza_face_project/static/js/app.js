
var pizzaApp = angular.module('pizzaApp',[]);


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
     });
     
     $scope.add = function(event){
       //if (event.keyCode == 13){
         $http.post("/userdetails/",{ dob: '1998-08-08' , gender:'M',  allergies:$scope.new_userpro,  diet: $scope.new_userpro, }).success(function(data){ 
           $scope.new_userpro = '';
           console.log('data');
           console.log(data);
            $scope.userpro.push(data);
           console.log('userpro is');
           console.log($scope.userpro);
         });
       //}
     }
});

