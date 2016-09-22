
var pairApp = angular.module('pairApp',[])
    .config(['$httpProvider', function($httpProvider) {
        // set CSRF for Django
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);



// Controller for pizzas
pairApp.controller('pairsController', function ($scope, $http, $rootScope ) {

    // urls
    var start_count = 0, time_start = 0, pairtime = 0, compsize = 0, curr =0;
    $scope.save_pairs = false;
    var pair_data = {};
    $scope.loadpizza = false;
    if (document.title == 'Choices'){
        start_count = 15;
        $scope.save_pairs = true;
        pair_data = $http.post("/choices/");
    }
    else if (document.title == 'Training'){
        start_count = 3;
        $scope.save_pairs=false;
        pair_data = $http.post("/train/");
    }

    var right_pizza=[], left_pizza =[], index_pair =[];
    $scope.round=1;
    $scope.countdwn= start_count;
    
    
    pair_data.then(function (response) {
        // set paramaters
      right_pizza = response.data.rights;
      index_pair = response.data.pairindex;
      left_pizza = response.data.lefts;
      next_pair(curr);
      $scope.loadpizza = true;
      compsize = index_pair.length;
      });
      
     var next_pair = function(i){
         console.log('i', i, time_start);
         // Sets new pairs
         $scope.rightside = right_pizza[i];
         $scope.leftside = left_pizza[i];
         $scope.indexs = index_pair[i];
         time_start = new Date().getTime();
         console.log('i', i, time_start);
     };
     
     var update_pair = function(){
        // catch end time
        var time_end = new Date().getTime();
        pairtime = time_end - time_start;
        console.log('time_end: ', time_end, '- time_start:', time_start, 'pairtime : ', pairtime);
        
        // PUT preferrance results and updates scope if in game mode
        if ($scope.save_pairs){
            var pk= $scope.indexs['id'];
            var data = {id: pk, index: $scope.indexs['index'], value: $scope.indexs['value'], time:pairtime };
            // update pair preferance
            $http.put("/pair/"+pk+"/",data).success(function(data){
                $scope.new_index = data;
            });
        }
        // if next pair not the last use them
        curr ++;
        if (curr<compsize){
            next_pair(curr);
            // Count down
            if ($scope.countdwn === 0 ){
                 $scope.round++;
                 reset_countdwn();
             }else $scope.countdwn = $scope.countdwn-1;
        }
        else{
            // if in game mode goto result page other wise give option if user ready to play
            if ($scope.save_pairs) window.location.href="/results/";
            else if (!$scope.save_pairs){ 
                var ready = confirm('Click OK if you are ready\nClick Cancel for more practice');
                if (ready) window.location.href="/choices/";
                else window.location.href="/train/";
            }
         }
     };
     
     $scope.lingd = {name: 'left', b:true};
     $scope.ringd = {name: 'right', b:true};
     // show ingredients list
     $scope.show = function(item){
         console.log(item.name, item.b );
         if (item.name === 'right' )item.b = !item.b;
         else item.b = !item.b;
     }
     
     // Countdown for rounds 
     var reset_countdwn = function(){
         console.log('gothere', $scope.round)
         if(curr == compsize){
             $scope.round='X';
             $scope.countdwn = 0;
         }
         else{
             switch ($scope.round) {
                 case 1:
                 case 2:
                     $scope.countdwn = 15;
                     break;
                 case 3:
                     $scope.countdwn = 20;
                     break;
                 case 4:
                     $scope.countdwn = 25;
                     break;
                 case 5:
                     $scope.countdwn = 30;
                     break;
                 default:
                     $scope.countdwn = 15;
             }
         }
         
     };
    
     // left likes
     $scope.prefLeft = function(){
         $scope.indexs['value'] = 1;
         update_pair();
     };
     
     // right likes
     $scope.prefRight = function(){
         $scope.indexs['value'] = 0;
         update_pair();
     };
     
});

