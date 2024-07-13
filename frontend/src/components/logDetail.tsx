import { Typography, Paper, IconButton } from "@mui/material";
import { useSelector } from "react-redux";
import KeyboardReturnIcon from "@mui/icons-material/KeyboardReturn";
import Grid from "@mui/material/Grid";
import { makeStyles } from "@mui/styles";
import { useDispatch } from "react-redux";
import { setCurrentScreen } from "../store/slices/navigationSlice";
import { AppDispatch } from "../store/store";

const style = makeStyles(() => ({
  returnButton: {
    display: "flex",
    justifyContent: "flex-start",
  },
}));

function LogsDetail() {
  const { logs } = useSelector((state: any) => state.log);
  const classes = style();
  const dispatch = useDispatch<AppDispatch>();

  const returnToList = () => {
    dispatch(setCurrentScreen("/"));
  };

  return (
    <Grid container spacing={2}>
      <Grid item className={classes.returnButton} xs={42} md={12} lg={12}>
        <IconButton onClick={returnToList}>
          <KeyboardReturnIcon />
        </IconButton>
      </Grid>
      <Grid item xs={2} md={12}>
        <Paper elevation={3} style={{ padding: 2, overflow: "auto" }}>
          <Typography
            variant="body2"
            component="pre"
            style={{ whiteSpace: "pre-wrap", textAlign: "left" }}
          >
            {logs}
          </Typography>
        </Paper>
      </Grid>
    </Grid>
  );
}

export default LogsDetail;
