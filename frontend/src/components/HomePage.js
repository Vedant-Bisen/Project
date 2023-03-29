import React, { Component } from "react";
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";
import ViewPlaylistPage from "./ViewPlaylistPage";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
} from "react-router-dom";

export default class HomePage extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Router>
        <Switch>
          <Route exact path="/">
            <p>This is the not the HomePage page</p>
          </Route>
          <Route path="/join" component={ViewPlaylistPage} />
          <Route path="/create" component={CreateRoomPage} />
          <Route path="/viewplaylist" Component={ViewPlaylistPage} />
        </Switch>
      </Router>
    );
  }
}
