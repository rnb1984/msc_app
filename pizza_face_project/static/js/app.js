
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
    var pairdata = $http.post("/test/");
    var compsize = 0, curr =0;
    var right_pizza=[], left_pizza =[], index_pair =[];
    $scope.round=1;
    $scope.countdwn=10;
    
    
    pairdata.then(function (response) {
        // set paramaters
      right_pizza = response.data.rights;
      index_pair = response.data.pairindex;
      left_pizza = response.data.lefts;
      next_pair(curr);
      compsize = index_pair.length;
      
      console.log(response.data);
      });
      
     var next_pair = function(i){
         // Sets new pairs
         $scope.rightside = right_pizza[i];
         $scope.leftside = left_pizza[i];
         $scope.indexs = index_pair[i];
         console.log(right_pizza);
         console.log($scope.indexs);
         console.log($scope.leftside);
     };
     
     var update_pair = function(){
         // Posts preferrance results and updates scope
         var pk= $scope.indexs['id'];
        
         var data = {id: pk, index: $scope.indexs['index'], value: $scope.indexs['value'] };
             console.log(data, pk)
        $http.put("/pair/"+pk+"/",data).success(function(data){
                 $scope.new_index = data;
               console.log(data);
             });
        
        console.log($scope.countdwn);
         if ($scope.countdwn < 1 ){
             $scope.round++;
             reset_countdwn($scope.round, $scope.round);
         }
         else{ $scope.countdwn = $scope.countdwn-1}
        
        console.log($scope.countdwn,$scope.round);
        console.log(curr);
        if (curr<compsize){
             next_pair(curr++);
         }
        else{
             console.log(curr,compsize, 'end got to page' );
             window.location.href="https://pizza-face-site-robertburry.c9users.io/test/predict/";
         }
     };
     $scope.lingd = {name: 'left', b:false};
     $scope.ringd = {name: 'right', b:false};
     $scope.show = function(item){
         console.log(item.name, item.b );
         if (item.name === 'right' )item.b = !item.b;
         else item.b = !item.b;
     }
     
     var reset_countdwn = function(round){
         if (round == 4){
             $scope.countdwn = 20;
         }
         else if(curr == compsize){
             $scope.round=4;
             $scope.countdwn = 0;
         }
         else{
             $scope.countdwn = 15;
         }
     };
    
     // left likes
     $scope.prefLeft = function(){
         // set pair oject values
         $scope.indexs['value'] = 1;
         update_pair();
     };
     
     // right likes
     $scope.prefRight = function(){
         
         // set pair oject values
         $scope.indexs['value'] = -1;
         update_pair();
     };
     
});

