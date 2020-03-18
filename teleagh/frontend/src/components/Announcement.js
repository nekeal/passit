import React, {useState} from "react";
import { Paper, Typography, Link } from "@material-ui/core";
import Icon from "./Icon";
import styled from "styled-components";
import styleHelpers from "../consts/styles";

const AnnouncementContainer = styled(Paper)`
  ${styleHelpers.gradientBorder};
  padding: 1rem;
  margin-bottom: 1rem;
  
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
    display: ${props => props.expanded ? 'flex' : 'none'};
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

function Announcement({ announcement }) {
  const [ expanded, setExpanded ] = useState(false);
  const { title, content, date, author } = announcement;
  return (
    <AnnouncementContainer variant="outlined" expanded={expanded ? 1 : 0}>
      <Typography variant="h6">
        { title }
      </Typography>
      <div className="content" onClick={() => setExpanded(!expanded)}>
        { content }
      </div>
      <div className="attachments">
        <Link href='/' target='_blank'>
          <div className="attachment">
            file1.jpg
            <Icon name="download"/>
          </div>
        </Link>
      </div>
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

export default Announcement;
