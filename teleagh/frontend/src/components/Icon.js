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

const icons = {
  eyeClosed: eye_closed,
  eyeOpen: eye_open,
  calendar: calendar,
  home: home,
  resources: resources,
  lecturer: lecturer,
  meme: meme,
  settings: settings,
  profile: profile,
  download: download,
  link: link,
  pdf: pdf,
  photo: photo,
  accept: accept,
  decline: decline
};

const sizes = {
  'small': '1.25rem',
  'normal': '1.5rem',
  'big': '1.75rem',
  'large': '2rem',
  'huge': '4rem'
};

function Icon({ name, size }) {
  const iconSrc = icons[name];
  const iconSize = sizes[size || 'normal'];
  return (
    <img src={iconSrc} alt="" style={{ height: iconSize }}/>
  );
}

export default Icon;
