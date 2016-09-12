
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
    
    // initate objects to populate/store form 
    $scope.user={}
    $scope.check = {allergies : [], diets: [] };
    $scope.ages = [{ code: 0, name:'20-25'},{ code: 1, name:'26-30'},{ code: 2, name:'30-34'},{ code: 3, name:'35-39'},{ code: 4, name:'40-44'},{ code: 5, name:'45-49'},{ code: 6, name:'50-54'},{ code: 7, name:'55-60'},{ code: 8, name:'60+'},{ code: 9, name:'undisclosed'}];
    $scope.occupations = [{ code: 0, name:'employed'},{ code: 1, name:'student'},{ code: 2, name:'graduate unemployed'},{ code: 3, name:'unemployed'},{ code: 4, name:'undisclosed'}];
    $scope.gender = [{name:'male', code:'M'},{name:'female', code:'F'}, {name:'other', code:'U'}];//$scope.gender = ['male','female','undisclosed'];
    $scope.allergies = ['none','dairy','egg','gluten','peanut','seafood','sesame','soy','sulfite','wheat','other'];
    $scope.diets= ['none','vegatarian','vegan','paleo','pescetarian', 'low-carb', 'other'];
    
    // coolects list of allegeries/diets
    $scope.updateCheck = function(item, type){
        $scope.check[type].push(item);
    };

    // On-Click check if form is vald and send
    $scope.fill = function(){
        console.log('this is the user: ',$scope.user, '$scope.master', $scope.master );
        console.log( 'user form valid: $scope.userForm.$valid', $scope.userForm.$valid);

        if($scope.userForm.$valid === true){
            // save form details to origional JSON Document
            $scope.master['allergies'] = $scope.check['allergies'].join(',');
            $scope.master['diet'] = $scope.check['diets'].join(',');
            $scope.master['occupation'] = $scope.user.occupation;
            $scope.master['dob'] = $scope.user.age;
            $scope.master['gender'] = $scope.user.gender;
            
            console.log($scope.master, $scope.two);
            console.log('test', $scope.master['dob'], $scope.master['gender'],$scope.master['allergies'], $scope.master['diet'] );
            var form_data = $scope.master;
            var pk =  $scope.master['id'];
            
            console.log(form_data, 'pk', pk);
            
             $http.put("/userdetail/"+pk+"/",form_data).success(function(data){ console.log('data');
             // got to pizza pair choices
             window.location.href="/train/";
             console.log(data);
             }); 
            }
     };
});

