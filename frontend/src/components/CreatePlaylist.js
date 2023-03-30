import React, {Component} from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";


export default class CreatePlaylist extends Component {
    constructor(props){
        super(props);
    }

    render(){
        return(
            <Grid container spacing={1}>
                <Grid item xs={12}>
                    <Button variant="contained" color="primary" onClick={this.props.handleReload}>
                        Create
                    </Button>
                </Grid>
            </Grid>
        )
    }
}