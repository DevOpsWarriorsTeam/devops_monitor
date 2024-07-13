import { Container } from "../models";

interface ContainerSliceProps {
  containers: Container[];
  loading: boolean;
  currentEnvironment: string;
}

export default ContainerSliceProps;
