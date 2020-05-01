import styled from "styled-components";
import { Paper } from "@material-ui/core";

export const styleHelpers = {
  gradientBorder: `
      background: linear-gradient(#fff, #fff), linear-gradient(90deg, rgba(135,18,154,0.6) 40%, rgba(9,83,159,0.6) 100%);
      background-origin: padding-box, border-box;
      background-repeat: no-repeat;
      background-position-x: -0.5px;
      border: 2px solid rgba(0,0,0,0.12) !important;
      box-shadow: 0 4px 4px rgba(200, 204, 214, 0.25);
  `
};

export const EditDialog = styled(Paper)`
  width: 90%;
  border-radius: 1rem;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 1rem;
  
  .form {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-bottom: 2rem;
  }
  
  .form-field {
    width: 90%;
    margin-bottom: 0.5rem;
    margin-top: 0.7rem;
  }
`;
