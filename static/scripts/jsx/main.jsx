var Router = ReactRouter.Router,
    Route = ReactRouter.Route,
    IndexRoute = ReactRouter.IndexRoute,
    Link = ReactRouter.Link,
    browserHistory = ReactRouter.browserHistory;


var MissingComponent = new React.createClass({
    render: function(){
        return (
            <div className="container">
                <h3>Comming soon ... </h3>
            </div>
        )
    }
});


React.render(
    (
        <Router history={browserHistory}>
            <Route path='/sample' component={MissingComponent}></Route>
        </Router>
    ),
    document.getElementById('content')
);
