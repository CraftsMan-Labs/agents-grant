import React from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import SignUp from './components/SignUp';
import SignIn from './components/SignIn';
import Chat from './components/Chat';
import './styles.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/signup" component={SignUp} />
          <Route path="/signin" component={SignIn} />
          <Route path="/chat" component={Chat} />
          <Route exact path="/">
            <Redirect to="/signin" />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
