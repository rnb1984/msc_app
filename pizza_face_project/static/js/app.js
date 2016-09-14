
var pairApp = angular.module('pairApp',[])
    .config(['$httpProvider', function($httpProvider) {
        // set CSRF for Django
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);



// Controller for pizzas
pairApp.controller('pairsController', function ($scope, $http, $rootScope ) {

    // urls
    console.log('got here', document.title);
    var COUNT = 0;
    $scope.save_pairs = false;
    var PAIRDATA = {};
    if (document.title == 'Choices'){
        COUNT = 10;
        $scope.save_pairs = true;
        PAIRDATA = $http.post("/choices/");
    }
    else if (document.title == 'Training'){
        COUNT = 3;
        $scope.save_pairs=false;
        PAIRDATA = $http.post("/train/");
    }

    var compsize = 0, curr =0;
    var right_pizza=[], left_pizza =[], index_pair =[];
    $scope.round=1;
    $scope.countdwn= COUNT;
    
    
    PAIRDATA.then(function (response) {
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
        // Posts preferrance results and updates scope if in game mode
        if ($scope.save_pairs){
            var pk= $scope.indexs['id'];
        
            var data = {id: pk, index: $scope.indexs['index'], value: $scope.indexs['value'] };
            console.log(data, pk)
            $http.put("/pair/"+pk+"/",data).success(function(data){
                 $scope.new_index = data;
               console.log(data);
            });
        }
        
        console.log($scope.countdwn);
        
         if ($scope.countdwn < 1 ){
             $scope.round++;
             reset_countdwn($scope.round, $scope.round);
         }
         else{ $scope.countdwn = $scope.countdwn-1}
        
        console.log($scope.countdwn,$scope.round);
        console.log(curr);
        
        // check if complete
        if (curr<compsize) next_pair(curr++);
        else{
            if ($scope.save_pairs) window.location.href="/results/";
            else if (!$scope.save_pairs) window.location.href="/choices/";
         }
     };
     
     $scope.lingd = {name: 'left', b:false};
     $scope.ringd = {name: 'right', b:false};
     // show ingredients list
     $scope.show = function(item){
         console.log(item.name, item.b );
         if (item.name === 'right' )item.b = !item.b;
         else item.b = !item.b;
     }
     
     // Countdown for rounds 
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
         console.log('got here');
         // set pair oject values
         $scope.indexs['value'] = 1;
         update_pair();
     };
     
     // right likes
     $scope.prefRight = function(){
         console.log('got here');
         // set pair oject values
         $scope.indexs['value'] = 0;
         update_pair();
     };
     
});

