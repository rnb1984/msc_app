
var expApp = angular.module('expApp',[])
    .config(['$httpProvider', function($httpProvider) {
        // set CSRF for Django
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);


// Controller for experiement one preferances
expApp.controller('expOneController', function ($scope, $http, $rootScope ) {
     // browser
     var get_agent = function(){
     /*global navigator*/
     var n = navigator.userAgent;
     if (n.match(/Chrome/i) != null) return 'Chrome';
        else if (n.match(/Opera/i) != null) return 'Opera/';
        else if (n.match(/Firefox/i) != null) return 'Firefox';
        else if (n.match(/Safari/i) != null) return 'Safari';
        else if (n.match(/IE/i) != null) return 'IE';
        else if (n.match(/Edge/i) != null) return '/Edge';
     };
     var agent = get_agent();

    // urls
    var start_count = 20, time_start = 0, pairtime = 0, compsize = 0, curr =0;
    var time_now = '';
    $scope.exp_finish = false;
    $scope.loadpizza = false;
    $scope.lingd = true, $scope.ringd = true;
    $scope.intermission = false;
    
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
         time_now = d.getHours()+' : ' + d.getMinutes();
         time_start = d.getTime();
     };
     
     var sendagain = function(pk,data){
         $http.put("/pair/"+pk+"/",data).success(function(data_out){
                if (data_out.value == 2) sendagain(pk,data);});
     };
     
     var update_pair = function(){
        // catch end time
        var time_end = new Date().getTime();
        pairtime = time_end - time_start;

        // PUT preferrance results and updates
        var pk= $scope.indexs['id'];
        var data = {
                id: pk,
                user : $scope.indexs['user'],
                index : $scope.indexs['index'],
                value : $scope.indexs['value'],
                time : pairtime,
                t_at : time_now, 
                browser : navigator.vendor + '|'+ navigator.appName +'|'+ agent,
                scrn_h : window.innerHeight,
                scrn_w : window.innerWidth,
                scroll_x : window.scrollX,
                scroll_y : window.scrollY,
                pic : $scope.expone,
                exp_no : $scope.indexs['exp_no'],
                slug : $scope.indexs['slug'],
                date : $scope.indexs['date'],
            };
        
        console.log(data.value,$scope.indexs['value']);
        console.log(data);

        // update pair preferance
        $http.put("/pair/"+pk+"/",data).success(function(data_out){
            // update pair preferance
            $scope.new_index = data_out;
            console.log(data_out.value);
            console.log(data_out);
            sendagain(pk,data);
        });
        
        var countdown = function(){
            // Count down
            if ($scope.countdwn === 1 ){
                 $scope.round++;
                 reset_countdwn();
             }else $scope.countdwn = $scope.countdwn-1;
        };
        // if next pair not the last use them0
        curr ++;
        if (curr<compsize){
            next_pair(curr);
            countdown();
        }
        else if (!$scope.exp_finish && curr<compsize*2){ 
                // Show distraction
                $scope.intermission = true;
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

