import React, { Component } from "react";
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";
import ViewPlaylistPage from "./ViewPlaylistPage";
import CreatePlaylistPage from "./CreatePlaylistPage";
import { Grid, Button, ButtonGroup, Typography } from "@material-ui/core";
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
    this.state = {
      roomCode: null,
    };
    this.clearRoomCode = this.clearRoomCode.bind(this);
  }

  async componentDidMount() {
    fetch("/api/user-in-room")
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          roomCode: data.code,
        });
      });
  }

  renderHomePage() {
    return (
      <Grid container spacing={3}>
        <Grid item xs={12} align="center">
          <Typography variant="h3" compact="h3">
            House Party
          </Typography>
        </Grid>
        <Grid item xs={8} align="center">
          <ButtonGroup disableElevation variant="contained" color="primary">
            <Button color="primary" to="/viewplaylist" component={Link}>
              View Playlist
            </Button>
            <Button color="primary" to="/createplaylist" component={Link}>
              Create Playlist
            </Button>
            <Button color="default" to="/join" component={Link}>
              Join a room
            </Button>
            <Button color="secondary" to="/create" component={Link}>
              Create a Room
            </Button>
          </ButtonGroup>
        </Grid>
      </Grid>
    );
  }

  clearRoomCode() {
    this.setState({
      roomCode: null,
    });
  }

  render() {
    return (
      <Router>
        <Switch>
          <Route
            exact
            path="/"
            render={() => {
              return this.state.roomCode ? (
                <Redirect to={`/room/${this.state.roomCode}`} />
              ) : (
                this.renderHomePage()
              );
            }}
          />
          <Route path="/join" component={RoomJoinPage} />
          <Route path="/viewplaylist" component={ViewPlaylistPage} />
          <Route path="/create" component={CreateRoomPage} />
          <Route path="/createplaylist" component={CreatePlaylistPage} />

          <Route
            path="/room/:roomCode"
            render={(props) => {
              return <Room {...props} leaveRoomCallback={this.clearRoomCode} />;
            }}
          />
        </Switch>
      </Router>
    );
  }
}
