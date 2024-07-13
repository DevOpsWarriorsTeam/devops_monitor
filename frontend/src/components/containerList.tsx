import { styled } from "@mui/material/styles";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import { FC } from "react";
import { Container } from "../models/models";
import ContainerCard from "./containerCard";
import { makeStyles } from "@mui/styles";

const style = makeStyles(() => ({
  title: {
    display: "flex",
    justifyContent: "flex-start",
  },
}));

const Demo = styled("div")(({ theme }) => ({
  backgroundColor: theme.palette.background.paper,
}));

const ContainerList: FC<{ containers: Container[] }> = ({ containers }) => {
  const classes = style();

  return (
    <Grid container spacing={2}>
      <Grid item className={classes.title} xs={4} md={12}>
        <Typography sx={{ mt: 4, mb: 2 }} variant="h4">
          Containers
        </Typography>
      </Grid>
      <Grid item xs={4} md={12}>
        <Demo>
          <List>
            {containers.map((container: Container) => (
              <ListItem key={container.id}>
                <ContainerCard name={container.name} id={container.id} />
              </ListItem>
            ))}
          </List>
        </Demo>
      </Grid>
    </Grid>
  );
};

export default ContainerList;
