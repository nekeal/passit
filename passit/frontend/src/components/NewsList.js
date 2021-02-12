import React, {useState} from "react";
import {IconButton, Input, InputAdornment, Typography} from "@material-ui/core";
import {Icon, News} from "./index";
import {USER_TYPES} from "../consts/options";
import {useTranslation} from "react-i18next";
import styled from "styled-components";
import {styleHelpers} from "../consts/styles";

const Container = styled.div`
  width: 100%;
  @media(min-width: 800px) {
    padding: 1rem;
    width: 45%;
  }

  .announcement-header {
    margin-bottom: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    img {
      margin-left: 0.8rem;
    }
    
    .news-search {
      border: unset;
      ${styleHelpers.gradientBorder};
      padding: 0.2rem;
      width: 100%;
      
      &::before, &::after {
        border: unset;
      }
      
      .MuiIconButton-root {
        padding: 0;
      }
      
      img {
        margin: 0 0.4rem;
      }
    }
  }

  .MuiInput-underline:hover:not(.Mui-disabled):before {
    border-bottom: none;
  }
`;

function NewsList({ newses, sags, profileInfo, onSearchReset, onSearchChange, onNewsEdit, onNewsDelete, onNewsAdd }) {
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchText, setSearchText] = useState("");
  const { t } = useTranslation();

  const mapNewses = newses => newses.map(news => {
    const { type } = profileInfo.defaultFag;
    const canEdit = type === USER_TYPES.REPRESENTATIVE || type === USER_TYPES.MODERATOR || news.isOwner;
    return <News
      key={news.id}
      sags={sags}
      news={news}
      canEdit={canEdit}
      onEdit={() => onNewsEdit(news)}
      onDelete={() => onNewsDelete(news)}
    />;
  });

  return (
    <Container>
      <div className="announcement-header">
        {
          searchOpen ? (
            <Input
              className="news-search"
              value={searchText}
              onChange={e => {
                const text = e.target.value;
                onSearchChange(text);
                setSearchText(text);
              }}
              placeholder={t("NEWS_SEARCH_PLACEHOLDER")}
              startAdornment={
                <Icon name="search"/>
              }
              endAdornment={
                <InputAdornment position="end">
                  <IconButton onClick={() => {
                    onSearchReset(); setSearchOpen(false); setSearchText("");
                  }}>
                    <Icon name="decline" clickable/>
                  </IconButton>
                </InputAdornment>
              }
            />
          ) : (
            <>
              <Typography variant="h6" >{t("ANNOUNCEMENTS")}</Typography>
              <div>
                <Icon name="search" size="big" clickable onClick={() => {
                  onSearchReset(); setSearchOpen(true); setSearchText("");
                }}/>
                <Icon name="add" size="big" clickable onClick={() => onNewsAdd()}/>
              </div>
            </>
          )
        }
      </div>
      { profileInfo && newses && mapNewses(newses)}
    </Container>
  )
}

export default NewsList;
