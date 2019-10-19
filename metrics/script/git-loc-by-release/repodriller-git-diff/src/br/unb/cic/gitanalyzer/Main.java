package br.unb.cic.gitanalyzer;

import org.repodriller.RepoDriller;
import org.repodriller.RepositoryMining;
import org.repodriller.Study;
import org.repodriller.filter.range.Commits;
import org.repodriller.persistence.csv.CSVFile;
import org.repodriller.scm.GitRemoteRepository;

import br.unb.cic.gitanalyzer.diff.Diff;

public class Main implements Study {
	private static String projectName;
	private static String projectURL;
	private static String tag1;
	private static String tag2;
	
	public static void main(String[] args)
    {
		projectName = "iris-test-aop-2"; //Enter the name of the project
		projectURL = "https://github.com/iris-email-client/iris-aspect-oriented-programming"; //Enter the project URL (github or directory)
		tag1 = ""; //Enter the name of the first tag
		tag2 = ""; //Enter the name of the second tag
		System.out.println("Process Started");
    	new RepoDriller().start(new Main());
        System.out.println("Process Completed!");
    }
	
	private static String fileNameToExport() {
		if (tag1 != null && tag2 != null) {
			return (System.getProperty("user.dir") + "/resources/" + projectName.replace(" ", "-") + "-" + tag1 + "-" + tag2 + ".csv").toLowerCase();
		}
		return (System.getProperty("user.dir") + "/resources/" + projectName.replace(" ", "-") + ".csv").toLowerCase();
	}

	public void execute() {
				new RepositoryMining()
				.in(GitRemoteRepository.singleProject(projectURL))
				//.through(Commits.betweenTags(tag1, tag2))
				.through(Commits.all())
				.process(new Diff(), new CSVFile(fileNameToExport())) //The results will ware exported on the 'resources' folder
				.mine();	
	}
}
