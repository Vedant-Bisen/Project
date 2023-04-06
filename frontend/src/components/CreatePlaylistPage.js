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

export default class CreatePlaylistPage extends Component {
  defaultName = "Playlist";
  defaultPublic = true;
  defaultCollaborative = false;
  defaultDescription = "Created with Spotify Party";

  constructor(props) {
    super(props);
    this.state = {
      playlistName: this.defaultName,
      public: this.defaultPublic,
      collaborative: this.defaultCollaborative,
      description: this.defaultDescription,
    };

    this.handlePlaylistButtonPressed =
      this.handlePlaylistButtonPressed.bind(this);
    this.handlePlaylistNameChange = this.handlePlaylistNameChange.bind(this);
    this.handlePublicChange = this.handlePublicChange.bind(this);
    this.handleCollaborativeChange = this.handleCollaborativeChange.bind(this);
    this.handleDescriptionChange = this.handleDescriptionChange.bind(this);
  }

  handlePlaylistButtonPressed() {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        playlistName: this.state.playlistName,
        public: this.state.public,
        collaborative: this.state.collaborative,
        description: this.state.description,
      }),
    };
    console.log(this.state.playlistName);
    console.log("sending request");
    fetch("/spotify/create-playlist", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        this.props.history.push("/viewplaylist");
      });
  }

  handlePlaylistNameChange(e) {
    this.setState({
      playlistName: e.target.value,
    });
  }

  handlePublicChange(e) {
    this.setState({
      public: e.target.value === "true" ? true : false,
    });
  }

  handleCollaborativeChange(e) {
    this.setState({
      collaborative: e.target.value === "true" ? true : false,
    });
  }

  handleDescriptionChange(e) {
    this.setState({
      description: e.target.value,
    });
  }

  render() {
    console.log(this.state.playlistName);
    console.log(this.state.public);
    console.log(this.state.collaborative);
    console.log(this.state.description);
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
            Create A Playlist
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl component="fieldset">
            <FormHelperText>
              <div align="center">Playlist Name</div>
            </FormHelperText>
            <TextField
              required={true}
              type="text"
              onChange={this.handlePlaylistNameChange}
              defaultValue={this.state.playlistName}
            />
          </FormControl>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl component="fieldset">
            <FormHelperText>
              <div align="center">Public</div>
            </FormHelperText>
            <RadioGroup
              row
              defaultValue={this.state.public.toString()}
              onChange={this.handlePublicChange}
            >
              <FormControlLabel
                value="true"
                control={<Radio color="primary" />}
                label="True"
                labelPlacement="bottom"
              />
              <FormControlLabel
                value="false"
                control={<Radio color="secondary" />}
                label="False"
                labelPlacement="bottom"
              />
            </RadioGroup>
          </FormControl>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl component="fieldset">
            <FormHelperText>
              <div align="center">Collaborative</div>
            </FormHelperText>
            <RadioGroup
              row
              defaultValue={this.state.collaborative.toString()}
              onChange={this.handleCollaborativeChange}
            >
              <FormControlLabel
                value="true"
                control={<Radio color="primary" />}
                label="True"
                labelPlacement="bottom"
              />
              <FormControlLabel
                value="false"
                control={<Radio color="secondary" />}
                label="False"
                labelPlacement="bottom"
              />
            </RadioGroup>
          </FormControl>
        </Grid>
        <Grid item xs={12} align="center">
          <FormControl component="fieldset">
            <FormHelperText>
              <div align="center">Description</div>
            </FormHelperText>
            <TextField
              required={true}
              type="text"
              onChange={this.handleDescriptionChange}
              defaultValue={this.state.description}
            />
          </FormControl>
        </Grid>
        <Grid item xs={12} align="center">
          <Button
            color="primary"
            variant="contained"
            onClick={this.handlePlaylistButtonPressed}
            defaultValue={this.defaultName}
          >
            Create A Playlist
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
