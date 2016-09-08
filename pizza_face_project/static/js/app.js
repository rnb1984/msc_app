
var pairApp = angular.module('pairApp',[])
    .config(['$httpProvider', function($httpProvider) {
        console.log('got here')
        // set CSRF for Django
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);


// Controller for pizzas
pairApp.controller('pairsController', function ($scope, $http ) {

    // urls
    var pairdata = $http.post("/test/"),
    compsize = 0;
    
    pairdata.then(function (response) {
      $scope.rightside = response.data.rights;
      $scope.indexs = response.data.pairindex;
      $scope.leftside = response.data.lefts; // todo
      compsize = response.data.pairindex.length;
      
      
      console.log(response.data)
      });
    
     // left likes
     $scope.prefLeft = function(item){
         // set pair oject values
         $scope.indexs[item]['value'] = 1;
         var pk= $scope.indexs[item]['id'];
         
       // angular.forEach($scope.new_index, function(i){
        //           console.log(i.id, pk, i.index, $scope.indexs[item]['index']);
        //           if (i.index === $scope.indexs[item]['index']){
        //               console.log( '---in',i);
         //              pk = i.id;
          //             $scope.indexs[item]['index'] = i.index;
        //               new_date = i.date;
          //             new_slug = i.slug; } });
        
         var data = {id: pk, index: $scope.indexs[item]['index'], value: $scope.indexs[item]['value'] };
         console.log(data, pk)
         $http.put("/pair/"+pk+"/",data).success(function(data){
             $scope.new_index = data;
           console.log(data);
         });
     };
     
     // right likes
     $scope.prefRight = function(item){
         console.log(item);
         
         // set pair oject values
         $scope.indexs[item]['value'] = -1;
         var pk= $scope.indexs[item]['id'];
         
         var data = {id: pk, index: $scope.indexs[item]['index'], value: $scope.indexs[item]['value'] };
         console.log(data, pk)
         $http.put("/pair/"+pk+"/",data).success(function(data){
             $scope.new_index = data;
           console.log(data);
         });
     };
     
});

