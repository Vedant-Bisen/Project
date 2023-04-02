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
      playlist_details: {},
    };
    this.handleReload = this.handleReload.bind(this);
    this.authenticateSpotify = this.authenticateSpotify.bind(this);
    this.getCurrentPlaylist = this.getCurrentPlaylist.bind(this);
  }


  getCurrentPlaylist() {
    fetch("/spotify/playlist").then((response) => {
      if (!response.ok) {
        return {};
      } else {
        return response.json();
      }
    }).then((data) => {this.setState({playlist_details: data})});
  }

  authenticateSpotify() {
    fetch("/spotify/is-authenticated")
      .then((response) => response.json())
      .then((data) => {
        this.setState({ spotifyAuthenticated: data.status });
        console.log(data.status);
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
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        playlist_id: this.state.Playlist_id,
        playlist_name: this.state.Playlist_name,
      }),
    };
    this.authenticateSpotify();
    this.getCurrentPlaylist();
    console.log("reloaded");
    fetch("/api/playlist-view", requestOptions).then((response) => {
      response.json().then((data) => {
        this.setState({
          Playlist_id: data.playlist_id,
          Playlist_name: data.playlist_name,
          Playlist_owner: data.playlist_owner,
          Playlist_url: data.playlist_url,
        });
      });
    });
    console.log(this.state.Playlist_id);
  }



  render() {
    return (
      <Grid container spaceing={1}>
        <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
            View Playlist
          </Typography>
        </Grid>
        {this.state.playlist_details.items  }
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
