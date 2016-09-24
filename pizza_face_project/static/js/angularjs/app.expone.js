
var expApp = angular.module('expApp',[])
    .config(['$httpProvider', function($httpProvider) {
        // set CSRF for Django
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);



// Controller for experiement one preferances
expApp.controller('expOneController', function ($scope, $http, $rootScope ) {

    // urls
    var start_count = 20, time_start = 0, pairtime = 0, compsize = 0, curr =0;
    var time_now = '';
    var pair_data = {} ;
    $scope.exp_finish = false;
    $scope.loadpizza = false;
    $scope.intermission = {name:'intermission', b:false};
    
    $http.post("/expone/start/").then(function (response) {
        var x = response.data.start;
        if (x % 2 == 0) $scope.expone= true;
        else if (x % 2 != 0)  $scope.expone= false;
    });

    var right_pizza=[], left_pizza =[], index_pair =[], right_pizza_p=[], left_pizza_p =[], index_pair_p =[];
    $scope.round=1;
    $scope.countdwn= start_count;
    
    // get all test pairs
    $http.post("/expone/image-pairs/").then(function (response) {
      // with pics
      right_pizza_p = response.data.pics.rights;
      index_pair_p = response.data.pics.pairindex;
      left_pizza_p = response.data.pics.lefts;
      
      // without pics
      right_pizza = response.data.nopics.rights;
      index_pair = response.data.nopics.pairindex;
      left_pizza = response.data.nopics.lefts;

      next_pair(curr);
      $scope.loadpizza = true;
      compsize = index_pair.length;
      });
     
     
     var next_pair = function(i){
         // Either with pics or without
         if($scope.expone ===true){
             $scope.rightside = right_pizza_p[i];
             $scope.leftside = left_pizza_p[i];
             $scope.indexs = index_pair_p[i];
         }else{
             $scope.rightside = right_pizza[i];
             $scope.leftside = left_pizza[i];
             $scope.indexs = index_pair[i];
         }
         var d = new Date();
         time_now = d.getHours()+' : ' + d.getMinutes()
         time_start = d.getTime();
     };
     
     var update_pair = function(){
        // catch end time
        var time_end = new Date().getTime();
        pairtime = time_end - time_start;

        // PUT preferrance results and updates
        var pk= $scope.indexs['id'];
        var data = {id: pk, index: $scope.indexs['index'], value: $scope.indexs['value'], time:pairtime, t_at:time_now};

        $http.put("/pair/"+pk+"/",data).success(function(data){
            $scope.new_index = data;
        });
        
        // update pairs research data
        /*global navigator*/
        data ={ browser : navigator.vendor + '|'+ navigator.appName +'|'+ navigator.userAgent, scrn_h : window.innerHeight, scrn_w : window.innerWidth, scroll_x : window.scrollX, scroll_y : window.scrollY, pic: $scope.expone};

        $http.put("/device/"+pk+"/",data).success(function(data){
            $scope.new_device = data;
        });
        var countdown = function(){
            // Count down
            if ($scope.countdwn === 1 ){
                 $scope.round++;
                 reset_countdwn();
             }else $scope.countdwn = $scope.countdwn-1;
        }
        // if next pair not the last use them0
        curr ++;
        if (curr<compsize){
            next_pair(curr);
            countdown();
        }
        else if (!$scope.exp_finish && curr<compsize*2){ 
                // Show distraction
                $scope.intermission.b = true;
                // Change pic for last round
                $scope.exp_finish = true;
                $scope.expone = !$scope.expone;
                next_pair(curr-compsize);
                countdown();
            }
        else if (curr<compsize*2){
            next_pair(curr-compsize);
            countdown();
        }
        else{
            // if experiment completed
            if ($scope.exp_finish) window.location.href="/expone/end/";
         }
     };
     
     $scope.lingd = {name: 'left', b:true};
     $scope.ringd = {name: 'right', b:true};
     // show ingredients list
     $scope.show = function(item){
         item.b = !item.b;
     }
     
     // Countdown for rounds 
     var reset_countdwn = function(){
         if(curr == compsize*2){
             $scope.round='X';
             $scope.countdwn = 0;
         }
         else $scope.countdwn = 20;
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

