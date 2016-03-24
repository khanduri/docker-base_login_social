var Router = ReactRouter.Router,
    Route = ReactRouter.Route,
    IndexRoute = ReactRouter.IndexRoute,
    Link = ReactRouter.Link,
    browserHistory = ReactRouter.browserHistory;


var MissingComponent = new React.createClass({
    render: function(){
        return (
            React.createElement("div", {className: "container"}, 
                React.createElement("h3", null, "Comming soon ... ")
            )
        )
    }
});


React.render(
    (
        React.createElement(Router, {history: browserHistory}, 
            React.createElement(Route, {path: "/sample", component: MissingComponent})
        )
    ),
    document.getElementById('content')
);
