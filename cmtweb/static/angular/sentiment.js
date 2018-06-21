// Define the `phonecatApp` module
var sentimentModule = angular.module('sentimentModule', []);

//http://localhost:5002/sentiment/trx/2018-04-29T22:16:12.069Z/2018-04-29T22:16:12.069Z
sentimentModule.controller('SentimentChartController', function SentimentChartController($scope, $http) {
  $http.get('http://localhost:5002/api/sentiment/eos/2018-04-29T22:16:12.069Z/2018-05-29T22:16:12.069Z').
        then(function(response) {
            $scope.greeting = response.data;
        });
});