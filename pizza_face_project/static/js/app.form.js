
var formApp = angular.module('formApp',[])
    .config(['$httpProvider', function($httpProvider) {
        // set CSRF for Django
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);



// Controller for pizzas
formApp.controller('formController', function ($scope, $http ) {

    // urls
    var user_data = $http.get("/userdetails/");
    
    user_data.then(function (response) {
      $scope.master = response.data;
    });
    $scope.form={ages:false, gender:false}
    $scope.check = {allergies : [], diets: [] };
    $scope.ages = ['20-25','26-30','30-34','35-39','40-44','45-49','50-54','55-60','60+','undisclosed'];
    $scope.occupations = ['employed', 'student', 'graduate unemployed', 'unemployed' ,'undisclosed'];
    $scope.gender = [{name:'male', value:'M'},{name:'female', value:'F'}, {name:'other', value:'U'}]; //$scope.gender = ['male','female','undisclosed'];
    $scope.allergies = ['none','dairy','egg','gluten','peanut','seafood','sesame','soy','sulfite','wheat','other'];
    $scope.diets= ['none','vegatarian','vegan','paleo','pescetarian', 'low-carb', 'other'];
    
    $scope.updateCheck = function(item, type){
        $scope.check[type].push(item);
    };
    
    // todo
    var isValid = function(type){
        console.log(type)
        if(!$scope.user[type]){
            $scope.form[type] = !$scope.form[type]; console.log(type, $scope.form[type])}
        return true
    }
    
    $scope.fill = function(){
        console.log('this is the user: ',$scope.user, '$scope.master', $scope.master );
        if(isValid('ages')){
        
        // check if all user files ar valid
        
        //$scope.master[0]['allergies'] = $scope.check['allergies'].join();
        //$scope.master[0]['diet'] = $scope.check['diets'].join();
        //$scope.master[0]['dob'] = $scope.user.age;
        $scope.master[0]['gender'] = $scope.user.gender;
        
        console.log($scope.master, $scope.master[0]);
        console.log('test', $scope.master[0]['dob'], $scope.master[0]['gender'],$scope.master[0]['allergies'], $scope.master[0]['diet'] );
        var form_data = $scope.master[0];
        var pk =  $scope.master[0]['id'];
        console.log(form_data, 'pk', pk);
         $http.put("/userdetails/"+pk+"/",form_data).success(function(data){ console.log('data');
         //window.location.href="https://pizza-face-site-robertburry.c9users.io/test/predict/";
         console.log(data);
         });
            
        }
     };

});

