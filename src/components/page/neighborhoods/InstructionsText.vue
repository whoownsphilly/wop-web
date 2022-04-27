<template>
  <div style="font-size: 18px">
    <sui-container>
      <sui-divider horizontal>Instructions</sui-divider>
      This is a search tool for open violations in the city. Please read the
      following instructions to help navigate this page:
      <sui-accordion exclusive>
        <sui-accordion-title>
          <sui-icon name="dropdown" />
          Searching Properties
        </sui-accordion-title>
        <sui-accordion-content>
          <p>
            Select a geographic area to find the 100 properties with the most
            violations in that area. These are properties that have an active
            rental license and violations are only counted if they occurred
            after 2018-01-01.
          </p>
          <p>
            Click <b>"Search By: Zip Code"</b> to enter a zip code as the
            geographic area of focus. Click <b>"Search By: Map Boundary"</b> to
            select your own geographic area of choice. You can do this either by
            zooming in on the map, or
            <i><b>by clicking one of the shapes on the map legend</b></i> and
            drawing a custom geographic area.
          </p>
          <p>
            Once you have selected a geographic area, click "Update Map", which
            will update the markers on the map to represent the 100 properties
            with the most violations within that area. The list below the map
            will also populate with this list.
          </p>
        </sui-accordion-content>
        <sui-accordion-title>
          <sui-icon name="dropdown" />
          Generating Lists
        </sui-accordion-title>
        <sui-accordion-content>
          <p>
            To generate custom lists, you first have to use the "+ Add List" tab
            to create a new list. Currently, each new list automatically gets
            assigned a different color. The system can reliably handle about 5
            lists at a time, but this could be increased in the future. After
            creating a list, you can click on a property marker in the map, it's
            address will pop up along with a drop-down menu with the populated
            list names, and a button that says 'Add to List'. By clicking on the
            address, it will then add that property to your own personal list,
            which can be subsequently downloaded.
          </p>
          <p>
            You can also bulk add properties to the list by going to that list's
            tab, using the selector tool on the map legend, drawing a shape on
            the map, and then clicking the 'Add map bounds to list' button.
          </p>
        </sui-accordion-content>
        <sui-accordion-title>
          <sui-icon name="dropdown" />
          Sharing Lists
        </sui-accordion-title>
        <sui-accordion-content>
          <p>
            After creating a list, you can share out 2 different types of links.
            There is a 'Link to read-only version of this List' which will link
            people directly to what is inside the Tab (a copy of the list and a
            map of just those selected properties). There is also a 'Link to
            walking directions' which will open up all of the selected
            properties in an external Google Maps page.
          </p>
          <p>
            If you are working on a list and are not completed with it, you can
            copy the URL (which changes whenever a property is added) and that
            URL should return you to the same list that you were working on.
          </p>
        </sui-accordion-content>
      </sui-accordion>
    </sui-container>
  </div>
</template>
