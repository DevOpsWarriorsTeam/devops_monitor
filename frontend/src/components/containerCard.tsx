import * as React from "react";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import { useDispatch } from "react-redux";
import { AppDispatch } from "../store/store";
import { getDevContainerLog } from "../store/slices/logSlice";
import { setCurrentScreen } from "../store/slices/navigationSlice";

interface Props {
  name: string;
  id: number;
}

export default function OutlinedCard({ name, id }: Props) {
  const dispatch = useDispatch<AppDispatch>();

  const handleGetLogs = () => {
    dispatch(getDevContainerLog(name));
    dispatch(setCurrentScreen("/logs"));
  };

  const card = (
    <React.Fragment>
      <CardContent>
        <Typography sx={{ fontSize: 12 }} color="text.secondary" gutterBottom>
          Container name:
        </Typography>
        <Typography variant="h5" component="div">
          {name}
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          ID: {id}
        </Typography>
      </CardContent>
      <CardActions>
        <Button size="small" onClick={handleGetLogs}>
          View Logs
        </Button>
      </CardActions>
    </React.Fragment>
  );

  return (
    <Box sx={{ minWidth: 660 }}>
      <Card variant="outlined">{card}</Card>
    </Box>
  );
}
