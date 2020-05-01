import React, {useState} from "react";
import { Paper, Typography, Link } from "@material-ui/core";
import Icon from "./Icon";
import styled from "styled-components";
import { styleHelpers } from "../consts/styles";
import IconButton from "@material-ui/core/IconButton";
import MoreVertIcon from "@material-ui/icons/MoreVert";
import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";
import ReactMarkdown from "react-markdown";
import { useTranslation } from "react-i18next";

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
    ${props => !props.expanded ? `
      max-height: 6rem;
      overflow: hidden;
    ` : `
      padding-bottom: 1rem;
    `};
  
    position: relative;
    
    &::before {
      content: "";
      display: block;
      position: absolute;
      width: 100%;
      height: 3rem;
      ${props => !props.expanded ? `
        top: 3rem;
        background: linear-gradient(0deg,rgba(255,255,255,1) 0%,rgba(255,255,255,0.8) 50%,rgba(255,255,255,0) 100%); 
      ` : `
        bottom: 0;
        background: transparent;
      `};
    }
    
    &-expand {
      position: absolute;
      height: 1rem;
      left: 50%;
      transform: translateX(-50%);
      cursor: pointer;
      color: rgba(9,83,159);
      ${props => !props.expanded ? `
        top: 4.5rem;
      ` : `
        bottom: 0;
      `};
    }
  }
  
  .attachment {
    margin-top: 1rem;
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
  const { t } = useTranslation();
  const open = Boolean(anchorEl);

  const { id, title, content, date, author, attachment } = news;

  return (
    <AnnouncementContainer variant="outlined" expanded={expanded ? 1 : 0}>
      <div className="header">
        <Typography variant="h6">{ title }</Typography>
        <div className="menu">
          {
            canEdit &&
              <>
                <IconButton onClick={event => setAnchorEl(event.currentTarget)} className="menu-icon"><MoreVertIcon /></IconButton>
                <Menu anchorEl={anchorEl} keepMounted open={open} onClose={() => setAnchorEl(null)}>
                  <MenuItem className="news-edit" onClick={() => { onEdit(); setAnchorEl(null); }}>{t("EDIT")}</MenuItem>
                  <MenuItem onClick={() => { onDelete(); setAnchorEl(null); }}>{t("DELETE")}</MenuItem>
                </Menu>
              </>
          }
        </div>
      </div>
      <div className="content">
        <ReactMarkdown source={content}/>
        <div className="content-expand" onClick={() => setExpanded(!expanded)}>{ expanded ? t("SHRINK") : t("EXPAND")}</div>
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
