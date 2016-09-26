
var formApp = angular.module('formApp',[])
    .config(['$httpProvider', function($httpProvider) {
        // set CSRF for Django
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);



// Controller for pizzas
formApp.controller('formController', function ($scope, $http ) {

    // urls
    var user_data = $http.get('/id/').then(function (response) { $scope.master = response.data;});
    var user_d = $http.get('/userdetails/').then(function (response) { $scope.two = response.data;});
    var user_nat = $http.get('/nationality/').then(function (response) { $scope.nationalities = response.data.nationality; console.log('got here', $scope.nationalities )});
    
    // initate objects to populate/store form 
    $scope.user={}
    $scope.check = {allergies : [], diets: [] };
    $scope.ages = [{ code: 0, name:'20-25'},{ code: 1, name:'26-30'},{ code: 2, name:'30-34'},{ code: 3, name:'35-39'},{ code: 4, name:'40-44'},{ code: 5, name:'45-49'},{ code: 6, name:'50-54'},{ code: 7, name:'55-60'},{ code: 8, name:'60+'},{ code: 9, name:'undisclosed'}];
    $scope.occupations = [{ code: 0, name:'employed'},{ code: 1, name:'student'},{ code: 2, name:'graduate unemployed'},{ code: 3, name:'unemployed'},{ code: 4, name:'undisclosed'}];
    $scope.gender = [{name:'male', code:'M'},{name:'female', code:'F'}, {name:'other', code:'U'}];
    $scope.allergies = {none: false, dairy:false, egg:false, gluten:false,peanut:false,seafood:false,sesame:false,soy:false,sulfite:false,wheat:false,other:false};
    $scope.diets= {none:false,vegatarian:false,vegan:false,paleo:false,pescetarian:false,lowcarb:false,other:false};
    
    
    // coolects list of allegeries/diets
    var updateCheck = function(){
        
        $scope.check['allergies']=[];
        $scope.check['diets']=[];

        for (var obj in $scope.allergies){
            console.log('in obj', obj, $scope.allergies[obj]);
            if ( $scope.allergies[obj] == true) $scope.check['allergies'].push(obj);
        }
        for (var obj in $scope.diets){
            console.log('in obj 2', obj, $scope.diets[obj]);
            if ($scope.diets[obj] == true) $scope.check['diets'].push(obj);
                }
        if ($scope.check['allergies'].length == 0)$scope.check['allergies']=['none'];
        if ($scope.check['diets'].length == 0)$scope.check['diets']=['none'];
            
    };

    // On-Click check if form is vald and send
    $scope.fill = function(){
        console.log('this is the user: ',$scope.user, '$scope.master', $scope.master );
        console.log( 'user form valid: $scope.userForm.$valid', $scope.userForm.$valid);
        updateCheck();

        if($scope.userForm.$valid === true){
            // save form details to origional JSON Document
            $scope.master['dob'] = $scope.user.age;
            $scope.master['gender'] = $scope.user.gender;
            $scope.master['allergies'] = $scope.check['allergies'].join(',');
            $scope.master['diet'] = $scope.check['diets'].join(',');
            $scope.master['occupation'] = $scope.user.occupation;
            $scope.master['nationality'] = $scope.user.nationality;
            
            var form_data = $scope.master;
            var pk =  $scope.master['id'];
            
             $http.put("/userdetail/"+pk+"/",form_data).success(function(data){
             // got to pizza pair choices
             if (document.title === 'Details') window.location.href="/train/";
             else window.location.href="/expone/train/";

             }); 
            }
     };
});

