const mailer = require('nodemailer');
const fs = require('fs');
require('dotenv').config();

function say(message) {
  if (process.env.VERBOSE) {
    console.log(message);
  }
}

say("Creating transport");
const transport = mailer.createTransport({
  host: 'smtp.gmail.com',
  port: 465,
  secure: true,
  auth: {
    user: process.env.USERNAME,
    pass: process.env.PASSWORD
  }
});

say("Reading file...");
const data = fs.readFileSync('./lastchance.txt', 'utf8').trim();


if (data.length > 0) {
  say("Sending email with data...");
  transport.sendMail({
    from: process.env.USERNAME,
    to: process.env.TARGET,
    subject: 'Found last chance products!',
    text: `${data}\n`
  }, (err, info) => {
    if (err) {
      console.error(err);
    } else {
      console.log(info);
    }
  });
} else {
  say("No data to send!");
}
