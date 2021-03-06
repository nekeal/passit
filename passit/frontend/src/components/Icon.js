import React from 'react';
import eye_closed from '../assets/eye_closed.png';
import eye_open from '../assets/eye_open.png';
import calendar from '../assets/calendar.png';
import home from '../assets/home.png';
import resources from '../assets/resources.png';
import lecturer from '../assets/lecturer.png';
import meme from '../assets/meme.png';
import settings from '../assets/settings.png';
import profile from '../assets/profile.png';
import download from '../assets/download.png';
import link from '../assets/link.png';
import pdf from '../assets/pdf.png';
import photo from '../assets/photo.png';
import accept from '../assets/accept.png';
import decline from '../assets/decline.png';
import add from '../assets/add.png';
import loader from '../assets/loader.gif';
import attachment from '../assets/attachment.png';
import search from '../assets/search.png';
import back from '../assets/back.png';

const icons = {
  eyeClosed: eye_closed,
  eyeOpen: eye_open,
  calendar,
  home,
  resources,
  lecturer,
  meme,
  settings,
  profile,
  download,
  link,
  pdf,
  photo,
  accept,
  decline,
  add,
  loader,
  attachment,
  search,
  back
};

const sizes = {
  'small': '1.25rem',
  'normal': '1.5rem',
  'big': '1.75rem',
  'large': '2rem',
  'huge': '4rem'
};

function Icon({ name, size, clickable, ...props }) {
  const iconSrc = icons[name];
  const iconSize = sizes[size || 'normal'];
  return (
    <img src={iconSrc} alt="" style={{ height: iconSize, cursor: clickable ? "pointer" : "initial" }} {...props}/>
  );
}

export default Icon;
