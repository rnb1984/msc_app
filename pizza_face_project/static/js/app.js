
var pairApp = angular.module('pairApp',[])
    .config(['$httpProvider', function($httpProvider) {
        // set CSRF for Django
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);



// Controller for pizzas
pairApp.controller('pairsController', function ($scope, $http, $rootScope ) {

    // urls
    var pair_count =0;
    var start_count = 0, time_start = 0, pairtime = 0, compsize = 0, curr =0;
    var time_now = '';
    $scope.save_pairs = false;
    var pair_data = {};
    $scope.lingd, $scope.ringd = true;
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
      console.log('index is',compsize);
      });
     
     
     var next_pair = function(i){
         // Sets new pairs
         $scope.rightside = right_pizza[i];
         $scope.leftside = left_pizza[i];
         $scope.indexs = index_pair[i];
         var d = new Date();
         time_now = d.getHours()+' : ' + d.getMinutes()
         time_start = d.getTime();
     };
     
     var update_pair = function(){
        // catch end time
        var time_end = new Date().getTime();
        pairtime = time_end - time_start;
        console.log('current is: ', curr);
        
        // PUT preferrance results and updates scope if in game mode
        if ($scope.save_pairs){
            var pk= $scope.indexs['id'];
            var data = {id: pk, index: $scope.indexs['index'], value: $scope.indexs['value'], time:pairtime, t_at:time_now};
            // update pair preferance
            $http.put("/pair/"+pk+"/",data).success(function(data){
                $scope.new_index = data;
                console.log('pair saved',pair_count);
                pair_count++;
            });
            
            // update pairs research data
            /*global navigator*/
            data ={ browser : navigator.vendor + '|'+ navigator.appName +'|'+ navigator.userAgent, scrn_h : window.innerHeight, scrn_w : window.innerWidth, scroll_x : window.scrollX, scroll_y : window.scrollY, pic: true};
            $http.put("/device/"+pk+"/",data).success(function(data){
                $scope.new_device = data;
            });
        }
        // if next pair not the last use them
        curr ++;
        if (curr<compsize){
            next_pair(curr);
            // Count down
            if ($scope.countdwn === 1 ){
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
    
     
     // Countdown for rounds 
     var reset_countdwn = function(){
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
                     $scope.countdwn = 35;
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

