import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import { Link } from "react-router-dom";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import { Collapse } from "@material-ui/core";

export default class ViewPlaylistPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      SpotifyAuthenticated: false,
      playlist_details: {
        playlist_id: [],
        playlist_name: [],
        playlist_owner: [],
        playlist_url: [],
      },
    };
    this.handleReload = this.handleReload.bind(this);
    this.authenticateSpotify = this.authenticateSpotify.bind(this);
    this.getCurrentPlaylist = this.getCurrentPlaylist.bind(this);
  }

  // componentDidMount() {
  //   this.interval = setInterval(this.handleReload, 1000);
  // }
  // componentWillUnmount() {
  //   clearInterval(this.interval);
  // }

  getCurrentPlaylist() {
    fetch("/spotify/playlist")
      .then((response) => {
        if (!response.ok) {
          return {};
        } else {
          return response.json();
        }
      })
      .then((data) => {
        this.setState({ playlist_details: data });
      });
  }

  authenticateSpotify() {
    fetch("/spotify/is-authenticated")
      .then((response) => response.json())
      .then((data) => {
        this.setState({ spotifyAuthenticated: data.status });
        // console.log(data.status);
        if (!data.status) {
          fetch("/spotify/get-auth-url")
            .then((response) => response.json())
            .then((data) => {
              window.location.replace(data.url);
            });
        }
      });
  }
  handleReload(e) {
    console.log("reloaded");
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    };
    this.authenticateSpotify();
    this.getCurrentPlaylist();
    console.log(this.state.playlist_details.playlist_name[0]);
  }

  render() {
    return (
      <Grid container spaceing={3}>
        <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
            View Playlist
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <Typography component="h6" variant="h6">
            <ul class="responsive-table">
              <li class="table-header">
                <div class="col col-1">Name</div>
                <div class="col col-2">Owner </div>
                <div class="col col-3">Site URL</div>
              </li>

              <li class="table-row">
                <div class="col col-1" data-label="Username">
                  {this.state.playlist_details.playlist_name.map((item) => {
                    return <div>item</div>;
                  })}
                </div>
                <div class="col col-2" data-label="Owner">
                  {this.state.playlist_details.playlist_owner.map((item) => {
                    return <div>item</div>;
                  })}
                </div>
                <div class="col col-3" data-label="Site URL">
                  {this.state.playlist_details.playlist_url.map((item) => {
                    return <div>item</div>;
                  })}
                </div>
              </li>
            </ul>
          </Typography>
        </Grid>
        ``
        <Grid item xs={12} align="center">
          <Button
            color="primary"
            variant="contained"
            onClick={this.handleReload}
          >
            Reload
          </Button>
        </Grid>
        <Grid item xs={12} align="center">
          <Button color="secondary" variant="contained" to="/" component={Link}>
            Back
          </Button>
        </Grid>
      </Grid>
    );
  }
}
