

class EmailTemplates:
    def title_verify(verification_link, title_id):
        return """<!DOCTYPE html>
              <html lang="en">
                <head>
                  <meta charset="UTF-8" />
                  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                  <title>console</title>
                </head>
                <body
                      style="
                        margin: 0;
                        padding: 0;
                        font-family: Arial, Helvetica, sans-serif;
                        background: #111111;
                        color: #fff;
                    ">
      <div class="container" style="position: relative">
      <div class="main" style="padding: 4.5rem 2.5rem">
        <div class="info" style="display: flex; justify-content: center">
          <svg1
            width="50"
            height="50"
            viewBox="0 0 56 56"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle cx="28" cy="28" r="28" fill="#242526" />
            <path
              d="M28.0078 27.998L28.0078 39.198"
              stroke="white"
              stroke-width="4"
              stroke-linecap="round"
            />
            <circle cx="28.0055" cy="18.732" r="2.4" fill="white" />
          </svg>
        </div>
        <h1
          class="title"
          style="
            text-align: center;
            font-size: 0.9rem;
            letter-spacing: 1px;
            color:#fff;
            margin: 1rem 0;
          "
        >
          JASIRI TITLE VERIFICATION
        </h1>
        <div
          class="description"
          style="
            display: grid;
            grid-template-rows: 1fr;
            color: #fff;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 0;
          "
        >
          <p style="line-height: 1.2rem; text-align: center; font-size: 0.8rem">
            This email contains identification and verification technology for
            electronic gadgets
          </p>
          <p style="line-height: 1.2rem; text-align: center; font-size: 0.8rem">
            When you click the button below from the device that you want to
            verify, it will detect that device and log its information to the
            Jasiri Web Console
          </p>
        </div>
        <div
          class="verify_div"
          style="padding: 1rem; display: flex; justify-content: center"
        >
          <div
            style="
              padding: 1.5rem 2rem;
              margin: auto;
              display: inline-block;
              border: 2px dotted #4c4c4c;
            "
          >
            <h1
              class="title"
              style="
                text-align: center;
                font-size: 1rem;
                letter-spacing: 1px;
                margin-bottom: 1rem;
              "
            >
              Title ID <br>
              #{title_id}
            </h1>
            <a
              style="
                background: #56e6b6;
                color: #111111;
                border: none;
                padding: 0.7rem;
                text-align: center;
                width: 280px;
                border-radius: 0.5rem;
                cursor: pointer;
              "
              href="{verification_link}"
            >
              
            CLICK TO VERIFY
          </a>
          </div>
        </div>
        <div
          class="last_description"
          style="
            display: grid;
            grid-template-rows: 1fr;
            color: #fff;
            gap: 0.5rem;
            padding: 0.5rem 0;
            margin-top: 1rem;
          "
        >
          <p style="line-height: 1.2rem; text-align: center; font-size: 0.8rem">
            If you did not sign up for this service please ignore this email
          </p>
          <a
            href="https://docs.jasiriprotocol.org/"
            target="_blank"
            style="
              font-size: 0.9rem;
              color: #56e6b6;
              text-align: center;
              font-weight: bold;
              cursor: pointer;
              text-decoration: none;
            "
          >
            READ THE JASIRI MANUAL FOR MORE
          </a>
          <p style="line-height: 1.2rem; text-align: center; font-size: 0.8rem">
            Thank You, Jasiri Team
          </p>
        </div>
        <div
          style="
          display: grid;
          grid-template-columns: 1.5rem 1fr !important;
          justify-content: center;
          color:#fff;
          align-items: center;
          gap: 0.7rem !important;
          font-size: 0.8rem;
          margin: 1rem auto;
          width: 281px;
          "
        >
          <span> © 2023 Safariblocks Ltd. All Rights Reserved.<span>
        </div>
      </div>
    </div>
  </body>
</html>""".format(verification_link=verification_link, title_id=title_id)