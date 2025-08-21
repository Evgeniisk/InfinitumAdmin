//So basically after defining all the versions of all the front-end dependencies including vite in package.json,
//and after running the nmp install command which installs everything in package.json,
//the package-lock.json file is created and the node_modules folder along with all the things in it is created by running this command.
//this vite.config.js file is then defined manually.

//Imports necessary modules from Vite:
import { defineConfig } from 'vite' //this imports the defineConfig function from Vite.
import vue from '@vitejs/plugin-vue' //this imports the Vue plugin for Vite.
//It enables Vite to handle Vue files (.vue), compile Vue components, and optimize them for the build process.

//Path and URL handling for the project:
import path from 'path'; // Imports Node.js 'path' module to handle and resolve file paths.
import { fileURLToPath } from 'url'; //Imports the 'fileURLToPath' function from Node.sjs's 'url' module to work with ES modules and resolve file URLs to file paths.

const __dirname = path.dirname(fileURLToPath(import.meta.url));
//'__dirname' is a variable used to reference the current directory. Since ES modules don't have '__dirname' by default, this line ensures the path os the current
//module's URL to a file path.

//Configuration of the vite project:
//https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  //base: Configures the base URL for the project, which can vary depending development or production mode.
  base:
      mode == "development"
          ? "http://localhost:5173/"
          : "/static/MainApp/spa/", //In production mdoe, the base URL will be a relative path for deployment (e.g., '/static/api/spa/').
  // build: Configures build-specific options
  build: {
      emptyOutDir: true, // Ensures that the output directory is emptied before a new build. This avoids leftover files from previous builds.
      outDir: path.resolve(__dirname, "../backend/MainApp/static/MainApp/spa"), //Specifies the output directory for the build project files. This will save to '../api/static/api/spa'.
  },
  //Plugins to extend vue's functionality
  plugins: [vue()], //tells Vite to use the Vue plugin to handle '.vue' files (single-file components) during development and the build process.
  //This secion configures module resolution.
  resolve: {
      alias: {
          '@': path.resolve(__dirname, './src'), //Sets up an alias for importing files from the 'src' folder.
      },
  },
}));