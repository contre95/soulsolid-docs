---
weight: 50
title: "Analyze"
description: "Metadata analysis feature"
icon: "article"
date: "2025-11-30T00:00:00+00:00"
lastmod: "2025-11-30T00:00:00+00:00"
draft: false
toc: true
---


<img src="/analyze_feat.jpg" alt="Analyze Feature" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px; margin: 10px 0;">
The analyze feature aims to run an analysis of the metadata of your library and fill those missing gaps.

<img src="/analyze_jobs.jpg" alt="Analyze Jobs" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px; margin: 10px 0;">

This is how the jobs logs look like. You'll be able to browse over these logs and see which tracks could be processed correctly and which tracks failed. For those which failed, you'll be able to manually fix them by clicking on `manual_fix="track"`.
At the moment, jobs for adding AcoustID and Lyrics are available. More analysis will be added in future releases of Soulsolid.
<style>
        .log-error { color: #ef4444 !important; font-weight: 500; }
        .log-warning { color: #f59e0b !important; font-weight: 500; }
        .log-violet { color: #8b5cf6 !important; font-weight: 500; }
        .log-blue { color: #3b82f6 !important; font-weight: 500; }
        .log-orange { color: #f97316 !important; font-weight: 500; }
        .log-green { color: #48AB84 !important; font-weight: 500; }
        .fullscreen-pre {
            width: 100vw;
            height: 100vh;
            overflow-y: auto;
            background-color: #000000;
            color: #e5e7eb;
            padding: 20px;
            box-sizing: border-box;
            white-space: pre-wrap;
        }
    </style>
<div class="mt-2 max-h-36 overflow-y-auto rounded border border-gray-300 dark:border-gray-700 bg-gray-100 dark:bg-black">
<pre class="p-2 text-xs text-gray-700 dark:text-gray-300 whitespace-pre-wrap" style="font-family: 'JetBrains Mono', 'Fira Code', 'Source Code Pro', monospace;" hx-get="/jobs/cde849ff-f9d7-419c-93ca-bc6868b8a3d0/logs?color=true" hx-trigger="load" hx-target="this" hx-swap="innerHTML" _="on htmx:afterSwap go to the bottom of me">time=2025-11-30T11:42:34.416+01:00 level=INFO msg="Starting job" name="Analyze Lyrics for Library"
<span class="log-pink">time=2025-11-30T11:42:34.416+01:00 level=INFO msg="EXECUTE STARTED: Lyrics job task is running" color=pink</span>
<span class="log-blue">time=2025-11-30T11:42:34.416+01:00 level=INFO msg="Enabled lyrics providers" providers="map[dummy:true lrclib:true]" color=blue</span>
<span class="log-blue">time=2025-11-30T11:42:34.416+01:00 level=INFO msg="Starting lyrics analysis" totalTracks=16 color=blue</span>
time=2025-11-30T11:42:34.416+01:00 level=INFO msg=Progress percentage=0 status="Starting analysis of 16 tracks"
time=2025-11-30T11:42:34.424+01:00 level=INFO msg=Progress percentage=0 status="Processing track 1/16: 4 + 20"
<span class="log-orange">time=2025-11-30T11:42:34.424+01:00 level=INFO msg="Skipping track with existing lyrics" trackID=5a56532c-9f5b-57d0-a9eb-c7e6f81cac77 title="4 + 20" lyricsLength=661 color=orange</span>
<span class="log-error">time=2025-11-30T11:42:36.890+01:00 level=ERROR msg="Failed to add lyrics for track" trackID=c3fded61-1a6b-5fbb-ac51-ce1ec30ae07c title="A contraluz" provider=lrclib error="failed to search lyrics with provider 'lrclib': no lyrics found" manual_fix="<a href="#" >track</a>"</span>
time=2025-11-30T11:42:36.890+01:00 level=INFO msg=Progress percentage=6 status="Processing track 2/16: Almost Cut My Hair"
<span class="log-orange">time=2025-11-30T11:42:36.890+01:00 level=INFO msg="Skipping track with existing lyrics" trackID=d4aaa7ad-27c1-5370-9c42-ce881e36cca3 title="Almost Cut My Hair" lyricsLength=656 color=orange</span>
time=2025-11-30T11:42:36.890+01:00 level=INFO msg=Progress percentage=6 status="Processing track 2/16: Carry On"
<span class="log-orange">time=2025-11-30T11:42:36.890+01:00 level=INFO msg="Skipping track with existing lyrics" trackID=3b3c0e60-3c8c-5694-8eed-213656355b0f title="Carry On" lyricsLength=906 color=orange</span>
<span class="log-green">time=2025-11-30T11:42:38.569+01:00 level=INFO msg="Lyrics analysis completed" totalTracks=16 processed=2 updated=0 skipped=14 color=green</span>
</pre>
</div>
<br>
(Scroll left to see the full log line)
