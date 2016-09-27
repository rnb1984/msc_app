
var pairApp = angular.module('pairApp',[])
    .config(['$httpProvider', function($httpProvider) {
        // set CSRF for Django
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);



// Controller for pizzas
pairApp.controller('pairsController', function ($scope, $http, $rootScope ) {
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
    var start_count = 0, time_start = 0, pairtime = 0, compsize = 0, curr =0;
    var time_now = '';
    $scope.save_pairs = false;
    var pair_data = {};
    $scope.lingd = true;
    $scope.ringd = true;
    $scope.loadpizza = false;
    if (document.title === 'Choices'){
        start_count = 15;
        $scope.save_pairs = true;
        pair_data = $http.post("/choices/");
    }
    else if (document.title === 'Training' || document.title === 'TrainEX' ){
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
         // Sets new pairs
         $scope.rightside = right_pizza[i];
         $scope.leftside = left_pizza[i];
         $scope.indexs = index_pair[i];
         var d = new Date();
         time_now = d.getHours()+' : ' + d.getMinutes();
         time_start = d.getTime();
     };
     
     var sendagain = function(pk,data){
         // if getting 2's back
         $http.put("/pair/"+pk+"/",data).success(function(data_out){
            console.log('second',data_out.value);
            console.log(data_out);
            if (data_out.value == 2)sendagain(pk,data);});
     };
     
     var update_pair = function(){
        // catch end time
        var time_end = new Date().getTime();
        pairtime = time_end - time_start;

        // PUT preferrance results and updates scope if in game mode
        if ($scope.save_pairs){
            var pk= $scope.indexs['id'];
            var data = {
                id: pk,
                index: $scope.indexs['index'],
                value: $scope.indexs['value'],
                time:pairtime,
                t_at:time_now, 
                browser : navigator.vendor + '|'+ navigator.appName +'|'+ agent,
                scrn_h : window.innerHeight,
                scrn_w : window.innerWidth,
                scroll_x : window.scrollX,
                scroll_y : window.scrollY,
                pic: true,
                exp_no : $scope.indexs['exp_no'],
                slug : $scope.indexs['slug'],
                date : $scope.indexs['date'],
            };
            // update pair preferance
            $http.put("/pair/"+pk+"/",data).success(function(data_out){
                // update pair preferance
                $scope.new_index = data_out;
                sendagain(pk,data);
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
                if (ready) {
                    if (document.title == 'TrainEX') window.location.href="/expone/image-pairs/";
                    else window.location.href="/choices/";
                }
                else {
                    if (document.title == 'TrainEX')window.location.href="/expone/train/";
                    else window.location.href="/train/";}
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

