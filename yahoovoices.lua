local url_count = 0


wget.callbacks.httploop_result = function(url, err, http_stat)
  -- NEW for 2014: Slightly more verbose messages because people keep
  -- complaining that it's not moving or not working
  local status_code = http_stat["statcode"]

  url_count = url_count + 1
  io.stdout:write(url_count .. "=" .. status_code .. " " .. url["url"] .. ".  \r")
  io.stdout:flush()

  if status_code >= 500 or 
  (status_code >= 401 and status_code ~= 404) then
    io.stdout:write("\nYahoo! Server returned "..http_stat.statcode..". Sleeping.\n")
    io.stdout:flush()

    os.execute("sleep 5")
    return wget.actions.CONTINUE
  end

  -- We're okay; sleep a bit (if we have to) and continue
  local sleep_time = 0.1 * (math.random(75, 125) / 100.0)

  if string.match(url["host"], "yimg%.com") then
    -- We should be able to go fast on images since that's what a web browser does
    sleep_time = 0
  end

  if sleep_time > 0.001 then
    os.execute("sleep " .. sleep_time)
  end

  return wget.actions.NOTHING
end

-- download URLs only once because wget is buggy
local downloaded_table = {}
wget.callbacks.download_child_p = function(urlpos, parent, depth, start_url_parsed, iri, verdict, reason)
  if verdict then
    if downloaded_table[urlpos["url"]["url"]] then
      return false
    else
      downloaded_table[urlpos["url"]["url"]] = true
      return true
    end
  else
    return verdict
  end
end

