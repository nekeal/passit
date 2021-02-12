import React, {useState} from "react";
import styled from "styled-components";
import { styleHelpers } from "../consts/styles";
import IconButton from "@material-ui/core/IconButton";
import MoreVertIcon from "@material-ui/icons/MoreVert";
import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";
import {useTranslation} from "react-i18next";

const Container = styled.div`
    ${styleHelpers.gradientBorder};
    padding: 0.8rem;
    margin-bottom: 1rem;
    position: relative;
    
    .content {
      margin-right: 1.5rem;
    }
    
    .menu {
      position: absolute;
      top: 0.4rem;
      right: 0.6rem;
      
      button {
        padding: 0.4rem;
      }
    }
    
    .author {
      margin-top: 0.6rem;
      text-align: right;
      color: rgba(55,54,54,0.7);
    }
`;

function Opinion({ opinion: { id, content, author }, onEdit, onDelete }) {
  const [ anchorEl, setAnchorEl ] = useState(null);
  const { t } = useTranslation();

  const open = Boolean(anchorEl);
  const canEdit = true;

  return (
    <Container>
      <div className="content">
        { content }
      </div>
      <div className="menu">
        {
          canEdit &&
          <>
            <IconButton onClick={event => setAnchorEl(event.currentTarget)} className="menu-icon"><MoreVertIcon /></IconButton>
            <Menu anchorEl={anchorEl} keepMounted open={open} onClose={() => setAnchorEl(null)}>
              <MenuItem className="opinion-edit" onClick={() => { onEdit(); setAnchorEl(null); }}>{t("EDIT")}</MenuItem>
              <MenuItem onClick={() => { onDelete(); setAnchorEl(null); }}>{t("DELETE")}</MenuItem>
            </Menu>
          </>
        }
      </div>

      <div className="author">{ author }</div>
    </Container>
  )
}

export default Opinion;
