import React, {useState} from "react";
import { Paper, Typography, Link } from "@material-ui/core";
import Icon from "./Icon";
import styled from "styled-components";
import styleHelpers from "../consts/styles";
import IconButton from "@material-ui/core/IconButton";
import MoreVertIcon from "@material-ui/icons/MoreVert";
import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";

const AnnouncementContainer = styled(Paper)`
  ${styleHelpers.gradientBorder};
  padding: 1rem;
  margin-bottom: 1rem;
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .menu-icon {
    padding: 0;
  }
  
  .content {
    cursor: pointer;
    margin-top: 1rem;
    
    ${props => !props.expanded && `
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    `}
  } 
  
  .attachment {
    margin-top: 1rem;
    //display: ${props => props.expanded ? 'flex' : 'none'};
    display: flex;
    align-items: center;
    font-style: italic;
    
    img {
      margin-left: 0.5rem;
    }
  }
  
  .info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: rgba(55,54,54,0.7);
    margin-top: 1rem;
  }
  
  .date {
    display: flex;
    align-items: center;
    
    div {
      margin-left: 0.5rem;
    }
  }
  
  .author {
    text-align: right;
  }

`;

function News({ news, canEdit, onEdit, onDelete }) {
  const [ expanded, setExpanded ] = useState(false);
  const [ anchorEl, setAnchorEl ] = useState(null);
  const open = Boolean(anchorEl);

  const handleClick = event => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const { id, title, content, date, author, attachment } = news;

  return (
    <AnnouncementContainer variant="outlined" expanded={expanded ? 1 : 0}>
      <div className="header">
        <Typography variant="h6">{ title }</Typography>
        <div className="menu">
          {
            canEdit &&
              <>
                <IconButton onClick={handleClick} className="menu-icon"><MoreVertIcon /></IconButton>
                <Menu anchorEl={anchorEl} keepMounted open={open} onClose={handleClose}>
                  <MenuItem onClick={() => { onEdit(news); handleClose(); }}>edytuj</MenuItem>
                  <MenuItem onClick={() => { onDelete(id); handleClose(); }}>usuń</MenuItem>
                </Menu>
              </>
          }
        </div>
      </div>
      <div className="content" onClick={() => setExpanded(!expanded)}>
        { content }
      </div>
      {
        attachment &&
        <div className="attachments">
          <Link href={attachment.link} target="_blank">
            <div className="attachment">
              { attachment.filename }
              <Icon name="download"/>
            </div>
          </Link>
        </div>
      }
      <div className="info">
        <div className="date">
          <Icon name='calendar' size='big'/>
          <div>{ date }</div>
        </div>
        <div className="author">{ author }</div>
      </div>
    </AnnouncementContainer>

  );
}

export default News;
